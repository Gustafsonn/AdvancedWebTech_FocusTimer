from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

account_bp = Blueprint('account', __name__)

@account_bp.route('/register/', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		existing_user = User.query.filter_by(username=username).first()
		if existing_user:
			flash("Username is already taken... Enter another.", "danger")
			return redirect(url_for('account.register'))

		hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

		new_user = User(username=username, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()

		flash("Account registered! You can now login.", "success")
		return redirect(url_for('account.login'))

	return render_template('account/register.html')


@account_bp.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		user = User.query.filter_by(username=username).first()

		if user and check_password_hash(user.password, password):
			session['user_id'] = user.id
			flash("User logged in", "success")
			return redirect(url_for('account.account_details'))
		else:
			flash("Invalid username or password", "danger")
			return redirect(url_for('account.login'))


	return render_template('account/login.html')


@account_bp.route('/logout/', methods=['POST'])
def logout():
	session.pop('user_id', None)

	flash("User logged out.", "success")

	return redirect(url_for('account.login'))


@account_bp.route('/')
def account_details():
	if 'user_id' in session:
		user = User.query.get(session['user_id'])
		return render_template('account/accountDetails.html')
	else:
		flash("You need to log in first", "warning")
		return redirect(url_for('account.login'))


@account_bp.route('/account/')
def no_account():
	return render_template('account/noAccount.html')
