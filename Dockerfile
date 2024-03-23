FROM python:3.9.5
COPY . /myocr
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone
WORKDIR ./myocr
RUN python -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip
#RUN pip --default-timeout=1688 install -i https://mirrors.aliyun.com/pypi/simple/ sklearn
#RUN pip --default-timeout=1688 install -i https://mirrors.aliyun.com/pypi/simple/ twisted-iocpsupport
RUN pip --default-timeout=1688 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
EXPOSE 6688
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6688", "--proxy-headers", "--forwarded-allow-ips='*'"]
