from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(200), nullable=False)

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(200), nullable=False)
	completed = db.Column(db.Boolean, default=False)
	task_list_id = db.Column(db.Integer, db.ForeignKey('task_list.id'), nullable=False)
	task_list = db.relationship('TaskList', backref=db.backref('tasks', lazy=True))

class TaskList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref=db.backref('task_lists', lazy=True))
