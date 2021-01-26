import random, string
from datetime import datetime as dt
from flask_restful import Resource, reqparse, abort, fields, marshal
from flask import Blueprint

from plugins import db, api
from app.User.model import User

user_bp = Blueprint('user', __name__, url_prefix='/api')


user_fields = {
  'id': fields.Integer,
  'nickname': fields.String,
  'avatar_url': fields.String,
  'school': fields.String,
  'phone': fields.String,
  'token': fields.String
}

class UserAPI(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('nickname', required=False)
    self.parser.add_argument('avatar_url', required=False)
    self.parser.add_argument('school', required=False)
    self.parser.add_argument('phone', required=True, help='phone number is not correct')

  # /api/users/<user_id>
  def get(self, user_id):
    # from flask import request
    # user = request.args.get('user')
    user=User.query.filter(User.id == user_id).all()
    return marshal(user, user_fields)

  # /api/users/<user_id>
  def post(self, user_id):
    args = self.parser.parse_args()
    nickname = args.nickname
    avatar_url = args.avatar_url
    school = args.school
    user = User.query.filter_by(user_id=user_id).first_or_404(description='no such user')
    
    # update nickname
    if nickname:
      user.nickname = nickname

    #  update avatar_url
    if avatar_url:
      user.avatar_url = avatar_url

    # update school
    if school:
      user.school = school

    # update to database
    db.session.commit()

    return marshal(user, user_fields), 201

class UsersAPI(Resource):

  # /api/users
  def get(self):
    return marshal(User.query.all(), user_fields), 200


'''
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from config import SMS
class SendSMSAPI(Resource):
  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('phone', help='phone is required')

    self.sms_sender = SmsSingleSender(SMS.APPID, SMS.APPKEY)

  def gen_sms_code(self):
    return ''.join(random.sample(string.digits, 4))

  # /api/sendsms
  def post(self):
    args = self.parser.parse_args()
    phone = args.phone
    phone_prefix = '86'
    template_id = 9722
    sms_sign = '' # 【腾讯云】
    sms_expire = 10 # min
    sms_code = self.gen_sms_code()
    # cache.set(sms_code)

    result = self.sms_sender.send_with_param(phone_prefix, phone,
      template_id, (sms_code, sms_expire), sign=sms_sign, extend="", ext="")

    return result
'''


class SiginAPI(Resource):

  def __init__(self):
    self.parser = reqparse.RequestParser(bundle_errors=True)
    self.parser.add_argument('phone', required=True, help='phone is required')
    # self.parser.add_argument('sms_code', required=True, help='sms_code is required')
    

  # /api/signin
  def post(self):
    args = self.parser.parse_args()
    phone = args.phone
    # sms_code = args.sms_code
    user = User.query.filter(User.phone == phone).all()

    # check sms
    # if sms_code != cache.get(sms_code):
    #   # wrong sms_code
    #   return josnify({'message':'wrong code}), 501
      

    if  len(user) == 1:
      # phone exits --->login
      pass
    else:
      # phone is not exists--->register
      user = User(
          nickname = phone,
          avatar_url = '',
          school = '',
          phone = phone,
          token = '',
      )
      db.session.add(user)
      db.session.commit()

    return marshal(user, user_fields), 201


  # def delete(self, user_id):
  #   user = User.query.filter_by(id=user_id).first_or_404(description=f'Can not delete {user_id}')
  #   db.session.delete(user)
  #   db.session.commit()

  #   return '', 204

api.add_resource(UserAPI, '/users/<user_id>')
api.add_resource(UsersAPI, '/users')
# api.add_resource(SendSMSAPI, '/sendsms')
api.add_resource(SiginAPI, '/signin')


