from datetime import datetime
from flask_restful import Resource, reqparse, abort, fields, marshal
from flask import Blueprint, jsonify

from plugins import db, api
from app.Course.model import Course
from app.User.view import user_fields
from app.User.model import User
from app.File.model import File
from app.File.view import file_fields

course_bp = Blueprint('course', __name__, url_prefix='/api')

course_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'managers': fields.List(fields.Nested(user_fields)),
  'repo_url': fields.String,
  'description': fields.String,
  'cover_url': fields.String,
  'isbn': fields.String,
  'created_time': fields.DateTime,
  'files': fields.List(fields.Nested(file_fields)),
}

def create_repo(name):
  return f'/repos/{name}'

class CoursesAPI(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('name', required=True, help='course name is required')
    self.parser.add_argument('user_id', required=True, help='user_id is required')
    self.parser.add_argument('decription', required=False)

  def get(self):
    '''
      uri: /api/courses
      Used to get all courses in database
    '''
    return marshal(Course.query.all(), course_fields), 200

  def post(self):
    '''
      uri: /api/courses
      A new course is created here
    '''

    args = self.parser.parse_args()
    name = args.name
    user_id = args.user_id
    user = User.query.filter(User.id == user_id).all()
    files = File.query.filter(Course.name == name).all()
    course = Course.query.filter(Course.name == name).all()
    if len( course ) == 1:
      # course already exists
      return marshal(course, course_fields), 409
    else:
      # create a new course here
      repo_url = create_repo(name)

      course = Course(
        name = name,
        managers = user,
        repo_url = repo_url,
        description = '计算机组成原理与技术',
        cover_url = '',
        isbn = '123456',
        created_time = datetime.now(),
        files = files
      )

      db.session.add(course)
      db.session.commit()
      return marshal(course, course_fields), 201

class CourseAPI(Resource):

  def get(self, course_id):
    '''
      uri: /api/courses/<course_id>
    '''
    return marshal(Course.query.filter(Course.id == course_id).all(), course_fields), 200


api.add_resource(CoursesAPI, '/courses')
api.add_resource(CourseAPI, '/course/<course_id>')