from plugins import db
from flask_restful import fields


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nickname = db.Column(db.String(32), index=True, unique=True, nullable=False)
  avatar_url = db.Column(db.String(128), index=False, nullable=True)
  school = db.Column(db.String(64), index=False, unique=False, nullable=True)
  phone = db.Column(db.String(11), index=True, unique=True, nullable=False)
  token = db.Column(db.String(128))

