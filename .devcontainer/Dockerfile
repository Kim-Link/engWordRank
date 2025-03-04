ARG python=python:3.12-slim


#---------------------------------------------
# 1) builder-stage
#---------------------------------------------

# 이미지를 생성
FROM ${python} AS builder-stage

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    gfortran \
    wget \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /home/backend/app

# pip 업그레이드 추가
RUN pip install --upgrade pip

# requirements 설치 전에 기본 패키지 설치
RUN pip install --no-cache-dir wheel setuptools

ENV PATH="/home/backend/.venv/bin:$PATH"


#---------------------------------------------
# 2) dev-stage: 개발 편의환경
#---------------------------------------------

# 이미지를 생성
FROM ${python} AS dev-stage

# 작업 디렉토리 생성
RUN mkdir -p /home/backend/app

# 기본 도구 설치
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# builder-stage의 /home/app/.venv를 build-image의 /home/app/.venv로 복사
COPY --from=builder-stage /home/backend/.venv /home/backend/.venv

# 가상 환경을 기본 실행 경로로 설정
ENV PATH="/home/backend/.venv/bin:$PATH"


# 작업 폴더를 /home/app로 설정(cd /home/app과 동일하다고 볼 수 있음)
WORKDIR /home/backend/app

# 빌드 컨텍스트의 모든 파일을 build-image의 /home/app으로 복사
COPY . /home/backend/app

# ENTRYPOINT ["/home/backend/app/.devcontainer/entrypoint.sh"]
CMD ["sh"]