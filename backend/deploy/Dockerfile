FROM python:3.10-slim

WORKDIR /app

COPY . .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000


CMD ["python", "main.py"]