from flask import Flask
from flask_restful import Api
from plugins import api, db
from app.User.view import user_bp
from app.Course.view import course_bp
from app.File.view import file_bp
from app.Git.Repo import repo_bp

def create_app():
  app = Flask(__name__, instance_relative_config=False)
  app.config.from_object('config.Dev')

  db.init_app(app=app)
  api.init_app(app=app)

  bps = [user_bp, course_bp, file_bp, repo_bp]

  for bp in bps:
    app.register_blueprint(bp)

  return app

  
