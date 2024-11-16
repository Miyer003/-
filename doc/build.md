# 部署文档

部署的环境将采用 `python3.10` 版本作为镜像

```mermaid
graph TD
    A[python3.10] --> B[flask]
    A --> C[nginx]
    B --> D[mysql]
    C --> D
```