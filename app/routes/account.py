from flask import Blueprint, request, jsonify, render_template

account_bp = Blueprint('account', __name__)

@account_bp.route('/register/')
def register():
	return render_template('account/register.html')

@account_bp.route('/login/', methods=['GET', 'POST'])
def login():
	return render_template('account/login.html')

@account_bp.route('/details/')
def account_details():
	return render_template('account/accountdetails.html')

@account_bp.route('/account/')
def no_account():
	return render_template('account/noAccount.html')
