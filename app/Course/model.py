from plugins import db

managers = db.Table('managers',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
  db.Column('is_present', db.Boolean)
)

class Course(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  managers = db.relationship('User', secondary=managers, lazy='subquery', backref=db.backref('courses', lazy=True))
  repo_url = db.Column(db.String, nullable=False)
  description = db.Column(db.String, nullable=False, default='一门好课')
  cover_url = db.Column(db.String)
  isbn = db.Column(db.String)
  created_time = db.Column(db.DateTime)
  files = db.relationship('File', backref='course', lazy=True)


