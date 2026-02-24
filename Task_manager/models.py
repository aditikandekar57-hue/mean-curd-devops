from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()

class User(UserMixin,bd.Model):
    id = db.Column(db.Integer,primary_key=True)
    usernme = db.Column(db.string(100),unique = True,nullable=False)
    password = db.Column(db.String(200),nullable = False)

    tasks = db.relationship('Task',backref = 'owner',lazy=True)

    class Task(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        content = db.Column(db.string(200),unique = True,nullable=False)
        complete = db.Column(db.Boolean(200),default = False)
        User_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
