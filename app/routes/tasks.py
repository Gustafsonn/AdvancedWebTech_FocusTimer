from flask import Blueprint, render_template

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/')
def tasks():
	return render_template('tasks.html')

@tasks_bp.route('/newTaskList/')
def new_task_list():
	return render_template('newTaskList.html')

@tasks_bp.route('/taskListInfo/')
def task_list_info():
	return render_template('taskListInfo.html')
