FROM python:3.12.4-slim

WORKDIR /app

COPY . /app

RUN pip3 install flask google-generativeai Pillow

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
