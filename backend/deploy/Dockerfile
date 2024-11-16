FROM python:3.10

WORKDIR /app

COPY . /app
# 安装 opencv 的依赖
RUN apt-get update && apt-get install -y libgomp1 libgl1-mesa-glx

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./deploy/requirements.txt

CMD ["python3", "main.py"]