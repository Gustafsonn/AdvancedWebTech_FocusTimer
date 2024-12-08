from flask import Flask
from .models import db
from .routes.account import account_bp
from .routes.tasks import tasks_bp
from .routes.general import general_bp
from .config import Config

def create_app():
	app = Flask(__name__)

	app.config.from_object(Config)	

	db.init_app(app)

	app.register_blueprint(account_bp, url_prefix='/account')
	app.register_blueprint(tasks_bp, url_prefix='/tasks')
	app.register_blueprint(general_bp)

	return app
