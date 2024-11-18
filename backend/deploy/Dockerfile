FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制项目代码到容器
COPY . /app

# 安装 OpenCV 所需的依赖
RUN apt-get update && apt-get install -y libgomp1 libgl1-mesa-glx

# 安装 Python 依赖
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./deploy/requirements.txt

ENV FLASK_APP=main.py
# 开放 5000 端口
EXPOSE 5000


CMD ["python3", "main.py"]