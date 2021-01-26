from datetime import datetime
from flask_restful import Resource, reqparse, abort, fields, marshal
from flask import Blueprint, jsonify

from plugins import db, api
from app.File.model import File
from app.User.view import user_fields
from app.User.model import User
from app.Course.model import Course

file_bp = Blueprint('file', __name__, url_prefix='/api')

file_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'file_type': fields.String,
  'contributes': fields.List(fields.Nested(user_fields)),
  'file_url': fields.String,
  'created_time': fields.DateTime,
  'updated_time': fields.DateTime,
  'file_size': fields.Float,
  'file_info': fields.String,
  'course_id': fields.Integer
}

def create_file(repo_name, file_name):
  return f'/repos/{repo_name}/{file_name}'

def update_file(file_url):
  return f'/new/{file_url}'

class FilesAPI(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('name', required=True, help='file name is required')
    self.parser.add_argument('user_id', required=True, help='user_id is required')
    self.parser.add_argument('file_type', required=True, help='file type is required')
    self.parser.add_argument('file_info', required=False)

  def get(self, course_id):
    '''
      uri: /api/course/<course_id>/files
      Get all files of the course
    '''
    return marshal(File.query.filter(File.course_id == course_id).all(), file_fields), 200

  def post(self, course_id):
    '''
      uri: /api/course/<course_id>/files
      A new course is created here
    '''

    args = self.parser.parse_args()
    name = args.name
    file_type = args.file_type 
    user_id = args.user_id
    user = User.query.filter(User.id == user_id).all()
    file = File.query.filter(db.and_(Course.id == course_id, File.name == name)).all()
    if len(file) == 1:
      # File already exists
      return marshal({'name': name}, {'msg': fields.FormattedString('file {name} exists.')}), 409
    else:
      # create a new course here
      file_url = create_file(course_id, name)

      file = File(
        name = name,
        file_type = file_type,
        contributes = user,
        file_url = file_url,
        created_time = datetime.now(),
        updated_time = datetime.now(),
        file_size = 0.0,
        file_info = f'created {name}',
        course_id = course_id
      )

      db.session.add(file)
      db.session.commit()
      return marshal(file, file_fields), 201

class FileAPI(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('user_id', required=True, help='user_id is required')

  def get(self, course_id, file_id):
    '''
      uri: /api/course/<course_id>/file/<file_id>
    '''
    return marshal(File.query.filter(db.and_(Course.id == course_id, File.id == file_id)).all(), file_fields), 200

  def put(self, course_id, file_id):
    '''
      uri: /api/course/<course_id>/file/<file_id>
    '''
    args = self.parser.parse_args()
    user_id = args.user_id
    file = File.query.filter(db.and_(Course.id == course_id, File.id == file_id)).first()

    file.file_url = update_file(file.file_url)
    file.update_time = datetime.now()
    file.file_info = f'{file.name} updated'
    
    user_ids = [contribute.id for contribute in file.contributes]
    if user_id not in user_ids:
      user = User.query.filter(User.id == user_id).first()
      file.contributes.append(user)

    db.session.commit()
    return marshal(file, file_fields), 202

  def delete(self,course_id, file_id):
    pass





api.add_resource(FilesAPI, '/course/<course_id>/files')
api.add_resource(FileAPI, '/course/<course_id>/file/<file_id>')