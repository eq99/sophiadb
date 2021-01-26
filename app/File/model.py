from plugins import db

contributes = db.Table('contribute',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('file_id', db.Integer, db.ForeignKey('file.id'), primary_key=True),
  db.Column('update_time', db.DateTime)
)

class File(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  file_type = db.Column(db.String,)
  contributes = db.relationship('User', secondary=contributes, lazy='subquery', backref=db.backref('contributes', lazy=True))
  file_url = db.Column(db.String, nullable=False)
  created_time = db.Column(db.DateTime)
  updated_time = db.Column(db.DateTime)
  file_size = db.Column(db.Float)  # KB
  file_info = db.Column(db.String) # i.e. git commit message
  course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)


