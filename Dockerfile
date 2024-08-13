FROM python:3.12.4-slim

WORKDIR /app

# requirements.txt 파일을 컨테이너의 /app 디렉토리로 복사
COPY requirements.txt /app/

# 패키지 설치
RUN pip3 install -r requirements.txt

# 나머지 애플리케이션 파일 복사
COPY . /app

# Flask 애플리케이션 실행
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
