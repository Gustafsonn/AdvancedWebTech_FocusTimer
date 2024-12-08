import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-quess'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'

