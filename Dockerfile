FROM ubuntu:latest
#启用上海时区
ENV TZ=Asia/Shanghai

RUN sed -i s@/archive.ubuntu.com/@/mirrors.cloud.tencent.com/@g /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y python3.11 python3-pip ca-certificates


RUN mkdir /usr/app
WORKDIR /usr/app
COPY . /usr/app

RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
RUN pip config set global.trusted-host mirrors.cloud.tencent.com
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python3", "app.py","80"]