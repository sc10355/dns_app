FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install Flask requests -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 9090

CMD ["python", "fs_server.py"]

