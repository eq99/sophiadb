from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from plugins import db, api
#from app.user.model import User

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__=="__main__":
  manager.run()