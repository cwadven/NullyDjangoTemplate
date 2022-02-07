# NULLYS Django TEMPLATE

## Purpose Of Project

[edit . 2022-02-07]

- Django 기본 TEMPLATE

## Project Introduce

[edit . 2022-02-07]

- Github Clone 으로 Django 프로젝트를 빠르게 생성하기 위한 Template

## Project Duration

[edit . 2022-02-07]

2022-02-07 ~ 

## Technologies Used

[edit . 2022-02-07]

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

## Developer Information

[edit . 2022-02-07]

#### Developer

##### 👨‍🦱 이창우 (Lee Chang Woo)

- Github : https://github.com/cwadven

## Project Structure

[edit . 2022-02-07]

```
Project Root
├── 📂 config
│    ├── 📜 settings.py
│    ├── 🔒 ENV.py
│    ├── 📜 asgi.py
│    ├── 📜 urls.py
│    └── 📜 wsgi.py
│
├── 📂 App Name
│    ├── 📂 migrations                                                      
│    ├── 📜 admin.py                                
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    ├── 📜 tests.py
│    ├── 📜 urls.py
│    ├── 📜 views.py
│    └── 📜 modles.py                                     
│
├── 📂 App Name
│    ├── 📂 migrations                                     
│    ├── 📜 admin.py                                  
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    ├── 📜 tests.py
│    ├── 📜 urls.py
│    ├── 📜 views.py
│    └── 📜 modles.py  
│  
├── 📂 App Name
│    ├── 📂 migrations                                     
│    ├── 📜 admin.py                                  
│    ├── 📜 app.py
│    ├── 📜 forms.py
│    └ .....
│
├── 📂 temp_static
│    ├── 🖼 XXXXX.png                                     
│    ├── 🖼 XXXXX.png                                  
│    ├── 🖼 XXXXX.png
│    ├── 🖼 XXXXX.png
│    └ .....
│
├── 📂 templates
│    └── base.html    
│
├── 🗑 .gitignore                                        # gitignore
├── 🗑 requirements.txt                                  # requirements.txt
└── 📋 README.md                                        # Readme
```

## Usage

[edit . 2022-02-07]

### 1. 기본 설정

config 파일에 `ENV.py` 파일 생성 후, `SECRET_KEY` 정의

```text
SECRET_KEY = 'DJANGO_SECRET_KEY 정의'
```

### 2. temp_static 폴더 생성

- collectstatic 위한 의존성 폴더 생성

### 3. 서버 초기 설정

```shell
python manage.py migrate
```

```shell
python manage.py collectstatic --no-input
```

### 4. 서버 실행

```shell
python manage.py runserver
```

### ETC. GitHub Action 설정 (설정중)

```shell
python manage.py gitaction Action파일명 (option -n "파일명" -b "브랜치명" -s "push" -p "step명")

# 예제 
python manage.py gitaction blank -n 'CI/CD' -b 'master' -s 'push' -p '[{"name": "aaa", "run": "ccc"}, {"name": "bbb", "run": "ccc"}]'
```

**결과**
```yaml
name: CI/CD

on:
  push:
    branch: [ master ]

jobs:
  build:
    runs-on: self-hosted

    steps:
    - name: aaa
      run: |
        ccc

    - name: bbb
      run: |
        ccc
```