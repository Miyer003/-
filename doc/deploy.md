# deploy(Linux/Macos)

### 后端本地部署
后端使用 Flask 框架，并使用 **conda** 来进行环境管理，所以需要提前准备 [conda 环境](https://docs.anaconda.com/miniconda/)。

1. 使用 conda 初始化 python 环境

```shell
conda create --name yuyiwang python=3.12 
```

2. 激活 conda 环境
```shell
conda activate yuyiwang
```

3. 检查当前 python 环境
```shell
which python
# 输出样例：/Users/sailschwarz/miniconda3/envs/yuyiwang/bin/python
```

4. 安装依赖
```shell
cd backend
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./deploy/requirements.txt
```

5. 运行后端 server
```shell
python main.py
```

6. 删除 conda 环境
```shell
conda deactivate && conda env remove -n yunyiwang
```


### 前端本地运行

```shell
cd frontend
npm install
npm run serve
```


### 云服务部署流程
参考 [云服务部署](../.github/workflows/deploy.yaml)


