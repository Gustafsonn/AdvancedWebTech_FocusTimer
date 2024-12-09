from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from app.models import db, TaskList

tasks_bp = Blueprint('tasks', __name__)

def is_logged_in():
	return 'user_id' in session

@tasks_bp.route('/tasks/')
def tasks():
	if not is_logged_in():
		flash("Please log in first.", "danger")
		return redirect(url_for('account.login'))

	user_id=session['user_id']
	task_lists = TaskList.query.filter_by(user_id=user_id).all()
	return render_template('tasks/tasks.html', task_lists=task_lists)

@tasks_bp.route('/newTaskList/', methods=['GET', 'POST'])
def new_task_list():
	if not is_logged_in():
		flash("Please login first.","danger")
		return redirect(url_for('account.login'))

	if request.method == 'POST':
		title = request.form['title']
		tasks = request.form.getlist('tasks[]')

		if not title or not tasks:
			flash("Title and tasks are requires", "danger")
			return redirect(url_for('tasks.new_task_list'))

		tasks_with_status = [{"task": task, "completed": False} for task in tasks]

		user_id = session['user_id']
		new_task_list = TaskList(title=title, user_id=user_id, tasks=tasks)
		db.session.add(new_task_list)
		db.session.commit()

		flash("Task list created!", "success")
		return redirect(url_for('tasks.tasks'))

	return render_template('tasks/newTaskList.html')

@tasks_bp.route('api/get_tasks/<int:task_list_id>', methods=['GET', 'POST'])
def get_tasks(task_list_id):
	if not is_logged_in():
		return jsonify({"error": "Unauthorized access"}), 401

	user_id = session['user_id']

	if request.method == 'POST':
		session['current_task_list_id'] = task_list_id
		return jsonify({"message": "Task list is set"}), 200
	
	current_task_list_id = session.get('current_task_list_id')

	if current_task_list_id:
		task_list = TaskList.query.filter_by(id=current_task_list_id, user_id=user_id).first()

		if not task_list:
			return jsonify({"error": "No task list found"}), 404

		tasks = [{"task": t, "completed": False} for t in task_list.tasks]
		return jsonify({"tasks": tasks, "title": task_list.title})

	return jsonify({"error": "No task list has been selected from tasks"}), 400
