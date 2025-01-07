import numpy as np
import cv2
from scipy.ndimage import zoom, gaussian_filter, label
import json
from ultralytics import YOLO
import streamlit as st
import os

#YOLO 모델로 객체 탐지 -> 결과 시각화
def apply_yolo_and_extract_objects(image, model):
    results = model(image)
    boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
    
    box_image = image.copy()
    for box in boxes:
        x_min, y_min, x_max, y_max = box
        cv2.rectangle(box_image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
    
    return box_image

#시야결손 패턴 생성
def create_visual_field_pattern(image_shape, json_path, patient_id="3645"):
    with open(json_path) as fin:
        data = json.loads(fin.read()) #HVF 데이터(json 파일)
    
    if patient_id not in data['data']:
        st.error(f"해당 환자 ID({patient_id})의 데이터가 존재하지 않습니다.")
        return None
    
    patient_data = data['data'][patient_id] #특정 환자 데이터 가져오기
    
    def get_latest_exam(side_data):
        return max(side_data, key=lambda x: x.get('age', 0)) if side_data else None
    
    right_exam = get_latest_exam(patient_data.get('R', []))
    left_exam = get_latest_exam(patient_data.get('L', []))
    
    if not right_exam and not left_exam:
        st.error(f"환자 {patient_id}의 시야 데이터가 없습니다.")
        return None
    
    #HVF 데이터에서 결손 점수 계산
    def calculate_defect_score(hvf_data):
        return np.sum(40 - np.array(hvf_data))
    
    right_score = calculate_defect_score(right_exam['hvf']) if right_exam else float('-inf')
    left_score = calculate_defect_score(left_exam['hvf']) if left_exam else float('-inf')
    chosen_exam = right_exam if right_score > left_score else left_exam
    
    hvf_data = np.array(chosen_exam['hvf'])
    
    #결손 데이터에 따라 패턴 생성(dB값)
    defect_matrix = np.zeros_like(hvf_data, dtype=float)
    defect_matrix[(hvf_data >= 30) & (hvf_data <= 40)] = 1.0
    defect_matrix[(hvf_data >= 20) & (hvf_data < 30)] = 0.75
    defect_matrix[(hvf_data >= 10) & (hvf_data < 20)] = 0.5
    defect_matrix[hvf_data < 10] = 0.0
    
    zoom_factor = (image_shape[0] / defect_matrix.shape[0], image_shape[1] / defect_matrix.shape[1])
    large_defect_matrix = zoom(defect_matrix, zoom_factor, order=1)
    visual_field = gaussian_filter(large_defect_matrix, sigma=5)
    visual_field = (visual_field - visual_field.min()) / (visual_field.max() - visual_field.min())
    return visual_field

#결손 매트릭스를 원본 이미지에 적용
def apply_visual_field_defect(image, visual_field):
    defect_mask = (visual_field < 0.5).astype(np.uint8)
    blurred_image = cv2.GaussianBlur(image, (51, 51), sigmaX=15)
    defect_image = image.copy()
    for i in range(3):
        defect_image[:, :, i] = (
            defect_mask * blurred_image[:, :, i] +
            (1 - defect_mask) * image[:, :, i]
        )
    return defect_image

#이미지 리맵핑 (특정 영역 중심으로 크기 조정 및 이동)
def remap_image(image, visual_field):
    height, width = image.shape[:2]
    intact_region = visual_field > 0.5 #결손 없는 영역
    labeled_array, num_features = label(intact_region) #결손 없는 영역 라벨링
    if num_features == 0:
        return np.zeros_like(image)
    
    component_sizes = np.bincount(labeled_array.ravel())[1:]
    largest_component = np.argmax(component_sizes) + 1
    largest_region = (labeled_array == largest_component)
    
    y_coords, x_coords = np.where(largest_region)
    weights = visual_field[y_coords, x_coords]
    center_y = int(np.average(y_coords, weights=weights))
    center_x = int(np.average(x_coords, weights=weights))
    
    scale = 0.5
    new_height = int(height * scale)
    new_width = int(width * scale)
    resized = cv2.resize(image, (new_width, new_height))
    
    y_start = max(0, center_y - new_height // 2)
    x_start = max(0, center_x - new_width // 2)
    y_end = min(height, y_start + new_height)
    x_end = min(width, x_start + new_width)
    
    result = np.zeros_like(image)
    result[y_start:y_end, x_start:x_end] = resized[:y_end-y_start, :x_end-x_start]
    return result
    
#시야결손 영역에만 블러 효과를 적용
def apply_edge_blur_based_on_defect(image, visual_field, blur_strength=30):
    height, width = image.shape[:2]
    
    defect_mask = visual_field < 0.5 
    blur_strength = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
    blurred_image = cv2.GaussianBlur(image, (blur_strength, blur_strength), sigmaX=15)
    blurred_image = np.where(defect_mask[:, :, None], blurred_image, image)
    
    return blurred_image

#Streamlit 애플리케이션 실행
def main():
    st.title("녹내장 환자 시야 확보 영상 처리")
    
    patient_id = st.text_input("환자 ID를 입력하세요:", "3645")
    video_file = st.file_uploader("동영상 파일을 업로드하세요", type=["mp4", "avi", "mov"])
    json_path = st.text_input("HVF 데이터 JSON 경로:", "C:\\Users\\ojo85\\OneDrive - 한국외국어대학교\\의료영상처리이론및실습\\alldata.json")
    
    if st.button("처리 시작"):
        if not video_file:
            st.error("동영상 파일을 업로드하세요.")
            return
        if not json_path:
            st.error("HVF 데이터 JSON 경로를 입력하세요.")
            return
        
        # 업로드된 파일을 임시 저장
        video_path = os.path.join(os.getcwd(), "uploaded_video.mp4")
        with open(video_path, "wb") as f:
            f.write(video_file.read())
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            st.error("동영상을 열 수 없습니다.")
            return
        
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        visual_field = create_visual_field_pattern((frame_height, frame_width), json_path, patient_id)
        if visual_field is None:
            return
        
        model = YOLO('yolov8n.pt')
        output_path = os.path.join(os.path.dirname(video_path), "processed_video.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width * 3, frame_height))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            defect_frame = apply_visual_field_defect(frame, visual_field)
            yolo_frame = apply_yolo_and_extract_objects(frame, model)
            remapped_frame = remap_image(yolo_frame, visual_field)
            
            # 시야 결손 영역에만 블러 적용
            edge_blurred_frame = apply_edge_blur_based_on_defect(remapped_frame, visual_field)
            
            combined_frame = np.concatenate((frame, defect_frame, edge_blurred_frame), axis=1)
            out.write(combined_frame.astype(np.uint8))
        
        cap.release()
        out.release()
        st.success(f"처리 완료! 결과 파일 저장 경로: {output_path}")

if __name__ == "__main__":
    main()
