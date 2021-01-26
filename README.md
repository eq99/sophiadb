# 项目简介

本项目是 Sophia 的后端，负责数据的服务。

# 项目结构说明

`serve.py`: 用 create_app 创建, 配置，管理并运行一个 app 实例。
`config.py`: 项目的配置，这个配置文件起到一个承上启下的作用。
`.env`: 敏感配置，这个是私密的，不对外公开。
`plugins/`: 引入 flask-SQLAlchemy, flask-restful。
`app/`: 数据库 model 与相应的 view 。
`app/__init__.py`: APP 工厂。
