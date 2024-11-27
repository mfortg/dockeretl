FROM python:3.13-slim
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD main.py
