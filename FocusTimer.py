from flask import Flask, render_template
app = Flask(__name__)

@app.route('/home/')
def home():
	return render_template('home.html')

@app.route('/account/')
def account():
	return render_template('account.html')

@app.route('/account/register/')
def register():
	return render_template('register.html')

@app.route('/account/login/')
def login():
	return render_template('login.html')

@app.route('/account/details/')
def accountDetails():
	return render_template('accountDetails.html')

@app.route('/tasks/')
def tasks():
	return render_template('tasks.html')

@app.route('/tasks/newTaskList/')
def newTaskList():
	return render_template('newTaskList.html')

@app.route('/tasks/taskListInfo/')
def taskListInfo():
	return render_template('taskListInfo.html')

if __name__ == ("__main__"):
	app.run(host='0.0.0.0', debug=True)
