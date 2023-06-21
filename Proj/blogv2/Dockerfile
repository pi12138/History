FROM python:3.8
MAINTAINER pipipipip

WORKDIR /project/blogv2
COPY . .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ wheel \
    && pip install -i https://mirrors.aliyun.com/pypi/simple/ setuptools==45.2.0 \
    && pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirement.txt

EXPOSE 8200
CMD ["python", "manage.py", "runserver", "8200"]