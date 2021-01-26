from plugins import db

auth_types=('PHONE','WEICHAT')
auth_types_emun=db.Enum(*auth_types, name='auth_type')

class Auth(db.Model):
  __tablename__='auths'

  id = db.Column('auth_id', db.BigInteger, primary_key=True)
  auth_type = db.Column(auth_types_emun, nullable=False, server_default='PHONE')
  identifier = db.Column(db.String(128), unique=True, nullable=False)
  token = db.Column(db.String(128), nullable=False)