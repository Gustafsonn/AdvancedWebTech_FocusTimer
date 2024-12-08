from flask import Blueprint, render_template

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def home():
	return render_template('home.html')


@general_bp.route('/test')
def test():
	return render_template('test.html')
