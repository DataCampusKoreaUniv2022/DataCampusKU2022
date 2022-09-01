# 플랜테리어 식물 인식 X-ray

# 팀 소개

- 2022 데이터청년캠퍼스 고려대학교 6조
- 팀명 : 초식공룡 🦕
- 팀원 : 강채현, 김보경, 김한주, 남정재, 문영민, 정보근

# 프로젝트 소개

## X-ray

X-Ray는 아마존 프라임 비디오에서 제공하고 있는 서비스로, 영상 시청 중 특정 장면에 출연 중인 배우가 누구인지 알려주고, 에피소드에서 장면별로 구분하여 바로 가기도 제공하며, 관련된 부가적인 사진 등 콘텐츠들도 제공되고, 해당 장면에 흐르는 음악이 무엇인지 알려주기도 합니다.

저희는 이러한 X-ray 서비스를 실내 식물에 적용하여 플랜테리어를 시도하는 사람들에게 도움이 되는 서비스를 개발하고자 하였습니다. 실내 식물이 등장하는 유튜브 영상을 대상으로 X-ray 기능을 제공하는 서비스를 개발하였습니다.

## 주요 기능

- 식물 유튜브 영상을 캡처하여 어떤 식물인지 알려줌
- 각 식물의 상세 정보 조회
- 농사로 농촌정보포탈에서 해당 식물 정보 조회
- 오늘의집 구매링크 제공
- 식물 저장 도감 기능 제공

## 스택 구성

![Untitled](README%20e4ffc24a345949238559abbf92336495/Untitled.png)

- Backend
    - Linux Ubuntu 20.04 (WSL2)
    - Django Framework
    - CUDA GPU
        - 시각화: GeForce GTX 1060 3GB
- Frontend
    - Chrome Extension
    - HTML + CSS
    - JavaScript
- 연계 웹페이지
    - Youtube
    - 오늘의집
    - 농사로 : 농촌진흥청 농업기술포털

---

## 파일 구조

```
.
├── DINO_model                              # model directory
│   ├── ckpts                               # checkpoint path
│   │   └── 20_checkpoint_best_regular.pth  # checkpoint file (Download from Google Drive)
│   ├── config                              # config files
│   │   └── DINO
│   │       └── DINO_4scale.py              # Base model config
│   ├── datasets                            # dataset transform/augmentation codes
│   ├── dino_views.py                       # json model output for django server
│   ├── engine.py                           # train/test/eval code for main.py
│   ├── main.py                             # model execute code
│   ├── models                              # model train codes
│   ├── requirements.txt                    # required modules
│   ├── scripts                             # train/eval shell scripts
│   └── util                                # useful codes
│       ├── 20class_plant_coco_id2name.json # id-class matching json file
│       └── visualizer.py                   # make visualized output for dino_views.py
│ 
├── dino_django                             # django api server
│   ├── dino                                # dino model app
│   ├── dino_django                         # django setting
│   └── manage.py                           # run server
│ 
└── extension                               # chrome extension
    ├── dogam                               # 도감 html+js+css+..
    ├── templates                           # 상세정보 html+js+css+..
    ├── xray                                # xray 화면 html+js+css+..
    ├── background.js                       # communicate with django api server
    ├── page.js                             # edit youtube html
    ├── manifest.json                       # chrome extension settings
    ├── newicon-128.png
    └── newicon.png                         # extension icons
```

---

# 설치 및 실행
    
## Demo in Colab

<a href="https://colab.research.google.com/drive/1ZF4lu2UDAMWF_FohwEBI7aNqWlqX_-cv?usp=sharing"><img src="https://img.shields.io/badge/Demo-blue?style=flat-square&logo=googlecolab&#logoColor=white&link=https://colab.research.google.com/drive/1Zx0zZMmj5Zyuf6RDV4EzPnjmeupha7fS?hl=ko#scrollTo=NfANEW0mu8oN"/></a> 

https://colab.research.google.com/drive/1ZF4lu2UDAMWF_FohwEBI7aNqWlqX_-cv?usp=sharing

```python
# 아래 주요 명령어들은 전부 데모 파일 안에 작성되어 있습니다.

# clone github
!git clone https://github.com/DataCampusKoreaUniv2022/DataCampusKU2022.git

# Go to dino model folder
%cd DataCampusKU2022/DINO_model/

# Download weights. If not working, You can try click to download release on this web. 
!wget https://github.com/DataCampusKoreaUniv2022/DataCampusKU2022/releases/download/v1.0.0/checkpoint_best_regular.pth

# Download and unzip image datasets. If not working, You can try click to download release on this web.
!wget https://github.com/DataCampusKoreaUniv2022/DataCampusKU2022/releases/download/v1.0.0/dino_data.zip
!unzip dino_data.zip
```

## 구글 드라이브 링크

- **파일 경로 정리 노션**
    
    https://childlike-health-ab5.notion.site/Code-77e0a92c34724356832ee79677958e78
    
- 전체 파일 폴더 (학습, 데이터셋 등)
    
    https://drive.google.com/drive/folders/1NOeVkLNDvUa1HIswMUL6CKX76qQhUIrs?usp=sharing
    
- 최종 이미지 데이터셋 + Annotation
    
    `dataset/dino_data`
    
    https://drive.google.com/drive/folders/1MWX8tIL5itq8BloK7PehzPg3ZzmPSFRO?usp=sharing
    
- 최종 모델 체크포인트
    
    `dataset/DINO/logs/DINO/R50-MS4-res/checkpoint_best_regular.pth`
    
    https://drive.google.com/file/d/1-_7q5wRy1i_Wgan2qT0LeiItGFwVukka/view?usp=sharing
    
- 제출 파일 폴더
    
    https://drive.google.com/drive/folders/1kBhBOzFLJjsE9j-Tlvv9nxonb3NhaHc-?usp=sharing
    
- 기타 파일 폴더
    
    https://drive.google.com/drive/folders/11S8LZkAacI19tG6z-kEnQ1tVGC2CMEne?usp=sharing


## 공통

```
git clone https://github.com/DataCampusKoreaUniv2022/DataCampusKU2022.git
```

## Chrome Extension 설치

1. 주소창에 `chrome://extensions` 입력하여 구글 확장 프로그램 접속
2. `압축해제된 확장 프로그램을 로드합니다.` 클릭하여 `extension` 폴더 선택
    
    ![스크린샷 2022-08-26 오후 7.27.25.png](README%20e4ffc24a345949238559abbf92336495/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2022-08-26_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_7.27.25.png)
    
    ![Untitled](README%20e4ffc24a345949238559abbf92336495/Untitled%201.png)
    
3. (서버 배포 시) `extension/background.js` 의 `serverhost` 값을 서버에 맞게 설정
    
    ```jsx
    var serverhost = '(API 서버 주소)';
    ```
    

## DINO 설치

1. DINO 모델 폴더로 이동
    
    ```
    cd DINO_model
    ```
    
2. Pytorch와 torchvision 설치 [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/).
    
    ```
    # an example(linux, cuda 11.3):
    pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu113
    ```
    
3. requirements 설치
    
    ```
    pip install -r requirements.txt
    ```
    
4. CUDA 관련 모듈 설치 (MSDA 등)
    
    ```
    cd models/dino/ops
    python setup.py build install
    ```
    
5. 작동 테스트
    
    ```
    python test.py
    cd ../../..
    ```
    
6. 각 학습/평가/시각화 파일 실행

## Django API Server 실행

1. (배포 시) `dino_django/dino_django/settings.py`
    
    `ALLOWED_HOSTS` 에 서버주소 추가 (포트 X)
    
    ```
    ALLOWED_HOSTS = ['000.000.000.000']
    ```
    
2. django 디렉토리로 이동
    
    ```
    cd dino_django
    ```
    
3. 서버 실행
    
    ```
    python manage.py runserver # localhost
    python manage.py runserver 0.0.0.0:(포트번호) # 배포시, 기본값 8000
    ```

4. (DINO 학습 데이터 변경 시)
    
    `DINO_model/dino_views.py` 수정
    
    ```python
    model_config_path = "(config 파일 경로)"
    model_checkpoint_path = "(체크포인트 파일 경로)"
    
    with open('(id 클래스 json 파일 )') as f:
    ```
    
---

# 시연 화면

![시연영상_AdobeExpress.gif](README%20e4ffc24a345949238559abbf92336495/시연영상_AdobeExpress.gif)

![도감.gif](README%20e4ffc24a345949238559abbf92336495/도감.gif)

---

![KakaoTalk_Photo_2022-08-26-19-15-10.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-10.jpeg)

유튜브 플레이어 하단 조작 바 우측에 식물 X-ray 버튼을 추가하여 실내 식물 영상에서 X-ray를 실행할 수 있도록 했습니다.

![KakaoTalk_Photo_2022-08-26-19-15-15.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-15.jpeg)

X-ray 버튼을 누르면 서버와 통신하면서 결과 이미지를 받아와서 유튜브 플레이어 프레임 안에 X-ray 결과 화면을 출력합니다. 좌측의 버튼을 눌러 각 식물의 상세 정보를 볼 수 있습니다.

![KakaoTalk_Photo_2022-08-26-19-15-22 002.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-22_002.jpeg)

![KakaoTalk_Photo_2022-08-26-19-15-22 003.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-22_003.jpeg)

![KakaoTalk_Photo_2022-08-26-19-15-23 009.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-23_009.jpeg)

상세정보 페이지에서 식물에 대한 자세한 정보를 볼 수 있으며 농사로 포털에서 더 자세한 정보를 볼 수 있도록 페이지를 넘어갈 수 있습니다.

![KakaoTalk_Photo_2022-08-26-19-15-22 004.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-22_004.jpeg)

![KakaoTalk_Photo_2022-08-26-19-15-23 010.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-23_010.jpeg)

구매하기 링크를 누르면 해당 식물의 오늘의집 구매 사이트로 넘어갈 수 있습니다.

![KakaoTalk_Photo_2022-08-26-19-15-22 006.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-22_006.jpeg)

![KakaoTalk_Photo_2022-08-26-19-15-23 008.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-23_008.jpeg)

도감에 저장하기 버튼을 누르면 우측 상단의 Chrome Extension 아이콘을 눌러 나오는 도감에 현재 식물을 추가하여 다른 영상을 볼 때도 저장된 식물을 볼 수 있습니다.

![KakaoTalk_Photo_2022-08-26-19-15-23 009.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-23_009%201.jpeg)

![KakaoTalk_Photo_2022-08-26-19-15-23 011.jpeg](README%20e4ffc24a345949238559abbf92336495/KakaoTalk_Photo_2022-08-26-19-15-23_011.jpeg)

이미 도감에 등록된 식물은 등록되지 않으며, 도감 화면 우측 상단의 초기화 버튼을 눌러 도감을 초기화할 수 있습니다.
