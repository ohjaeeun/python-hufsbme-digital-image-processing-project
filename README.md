# Visual Field Supplementation Image Processing System for Patients with Glaucoma (2024)
[24-2 HUFS BME 의료영상처리 이론 및 실습] \
**team member** : 오재은, 이은서, 정혜교, 김유빈, 박지훈

> ## ⭐ Background
- 녹내장은 시신경 손상으로 인해 시야 결손이 발생하는 질환으로, 전 세계적으로 회복할 수 없는 가장 중요한 실명의 원인 중 하나이다.
- 녹내장 초기에는 주변 시야가 좁아지다가 점차 중심 시력까지 손상되는 양상을 보이며 이러한 시야 결손은 일상생활 중 운전, 계단 오르기, 물건 잡기 등의 활동에서 큰 위험을 초래한다.
- 최근 녹내장 환자의 시야 결손을 보완할 수 있는 VR, AR 기술이 개발되었지만  2D 이미지에만 국한된 테스트 및 이미지 품질 문제와 같은 한계가 있어, 우리 프로젝트에서는 기존 기술의 단점을 개선하여 프로젝트를 진행할 것이다. 

> ## ⭐ Vision
- 녹내장 환자가 **시야 결손**으로 인해 겪는 **일상 생활의 불편함을 최소화**하고, 보다 나은 시각적 경험을 제공하는 **맞춤형 영상 처리 시스템을 구축**하는 것을 목표로 한다.

> ## ⭐ Purpose & Method

1. **시야 결손을 분석 및 보완**
    - 녹내장 환자의 시야 결손 패턴을 분석하여 결손된 시야의 영향을 최소화할 수 있는 영상 보정 알고리즘을 개발한다. 이를 통해 일생 생활에서 녹내장 환자들의 원활한 시각 정보 인식을 돕는다.
2. **남아있는 시야 활용을 기반한 정보 인식 강화 알고리즘 개발**
    - 사용자의 남아있는 주변 시야를 기반으로 영상을 변형하여 중요한 정보를 한눈에 파악할 수 있도록 알고리즘 개발한다.
3. **시야 결손 보완을 위한 주변부 정보 이동**
    - 손상된 주변부 시야 정보를 자동으로 시야의 건강한 부분으로 이동하고 축소하는 리매핑 알고리즘을 통해, 결손된 시야를 보완한다.
4. **객체 강조 및 확대, 축소 기능을 통한 사용성 개선**
    - 객체 강조를 위한 영상처리로 YOLO 모델을 적용하여 사용자가 객체를 보다 잘 인지할 수 있도록 한다.
    - 영상의 확대 및 축소 기능을 통해, 사용자 맞춤형 시각 환경을 제공한다. 이는 실생활에서 사용자가 보다 쉽게 주변 환경을 인식하고, 독립적으로 활동할 수 있도록 도울 수 있다.
  
> ## ⭐Data

#### 1. 데이터 수집

- [1. UWHVF Dataset](https://www.notion.so/1-UWHVF-Dataset-1650013f595180eea546cfb7a43d2f22?pvs=21)

- [2. **Video Data**](https://www.notion.so/2-Video-Data-1650013f5951808291cfe388bdbdcdf7?pvs=21)

#### **2. 녹내장에 대한 기본 개념**

- [녹내장의 분류](https://www.notion.so/1650013f595180dd8566e60f1b4f9641?pvs=21)

> ## ⭐Algorithm

- [알고리즘 구현 과정](https://www.notion.so/5fd461c2d34e4aeea263aa1165ce35c1?pvs=21)

- [최종 코드](https://www.notion.so/4d2e9784855348a49643e9c5105948be?pvs=21)

> ## ⭐Result

→ Streamlit 시연 결과 (환자 ID: 3645)

[KakaoTalk_Video_2024-12-24-14-52-50-1.mp4](https://prod-files-secure.s3.us-west-2.amazonaws.com/d7c653f1-5e48-4e3b-9fb5-53ecd02f00a0/4edb69f7-abe8-47f8-a420-ce7f1641c7f0/KakaoTalk_Video_2024-12-24-14-52-50-1.mp4)

→ 시연 결과 2

[KakaoTalk_Video_2024-12-24-14-53-15.mp4](https://prod-files-secure.s3.us-west-2.amazonaws.com/d7c653f1-5e48-4e3b-9fb5-53ecd02f00a0/5137cf48-5b88-4792-a6cf-7de140ddc480/KakaoTalk_Video_2024-12-24-14-53-15.mp4)

> ## ⭐Future Works

1. 정상 영역으로 image Remapping 후 작아진 객체를 더욱 정확하게 인식할 수 있도록 모델의 성능을 개선시킬 수 있음.
→ 작은 물체에 대한 탐지 성능이 낮은 YOLO 모델의 한계.
→ 추후 **Faster R-CNN(YOLO보다는 조금 더 무겁지만 더 높은 성능의 객체 탐지)과 같은 모델**로 개선 가능.
2. 정상 시야 영역으로 이미지 축소 후에 생기는 좁은 시야로 인한 답답함과 거리감 상실을 해결하기 위해 생성형 AI를 활용한 이미지 확장을 통하여 결손된 부분이더라도 검은 화면이 보이는 것이 아닌 실제 시야처럼 보이도록 보완하거나 영상에 거리감을 인식할 수 있는 좌표를 추가.
→ 이를 통해 시야 보정 후의 물체에 대한 원근감을 해결할 수 있는 가능성이 높아질 수 있음.
3. 기존 연구의  Digital Spectacles보다 경량화된 알고리즘을 통해 추후 VR 기기와 같은 하드웨어 개발에 사용할 수 있음. 

> ## ⭐ Previous Studies

- Expansion of Peripheral Visual Field with Novel Virtual Reality Digital Spectacles
https://pmc.ncbi.nlm.nih.gov/articles/PMC7002244/pdf/nihms-1059599.pdf
→ **사용자 맞춤형 녹내장 환자의 시야 보완 시스템에 관한 기존 연구**. 이 연구에서는 시야 검사와 시야 보정을 Digital Spectacles 시스템에서 통합적으로 수행하는 것으로 확인되며 프로젝트의 주요 레퍼런스로 사용하였다.
- https://www.revieweducationgroup.com/ce/the-physical-manifestations-of-glaucoma-and-what-they-signify 
→ 녹내장 환자 초기, 중기, 말기의 유형이 나타나는 기존 연구.

> ## ⭐ Reference

- 녹내장 환자가 바라보는 시야 :
https://youtu.be/YG0W52e6Srs?feature=shared
