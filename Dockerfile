FROM python:3.12.4-slim
 
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app

WORKDIR /app
 
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
