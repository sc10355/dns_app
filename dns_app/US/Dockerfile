FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install Flask requests -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 8080

CMD ["python", "us_server.py"]

