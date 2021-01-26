
# Folder Struct Descrition

This folder defines apis whose data comes from a database.

The `__init__.py` in this folder defines the flask app factory.

The  `model/` folder defines models for SQLAlchemy.

The  `api/` folder defines apis for url.

# Naming Description

- A model name is singular like: User, Course, Comment, Role, Auth
- A table name is plural, like: users, courses, comments, auth, roles
- A api name is model name+API, like: UserAPI, AuthAPI, RoleAPI
