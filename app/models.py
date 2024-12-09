from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)

class TaskList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref=db.backref('task_lists', lazy=True))
	tasks = db.Column(db.PickleType, nullable=False)
