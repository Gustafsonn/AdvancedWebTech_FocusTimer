from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from app.models import db, TaskList, Task

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

	if not session.get('current_task_list_id') and task_lists:
		session['current_task_list_id'] = task_lists[0].id

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

		user_id = session['user_id']
		new_task_list = TaskList(title=title, user_id=user_id)

		for task_desc in tasks:
			new_task = Task(task=task_desc, task_list=new_task_list)
			db.session.add(new_task)

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
	task_list = TaskList.query.filter_by(id=task_list_id, user_id=user_id).first()

	if request.method == 'POST':
		session['current_task_list_id'] = task_list_id
		return jsonify({"message": "Task list is set"}), 200

	if not task_list:
		return jsonify({"error": "No task list found"}), 404

	tasks = [{"task": t.task, "completed": t.completed} for t in task_list.tasks]
	return jsonify({"tasks": tasks, "title": task_list.title})


@tasks_bp.route('api/get_first_incomplete_task', methods=['GET'])
def get_first_incomplete_task():
	task_list_id = request.args.get('task_list_id')

	if not task_list_id:
		return jsonify({"error": "Task list not found"}), 404

	try:
		task_list = TaskList.query.filter_by(id=task_list_id, user_id=session['user_id']).first()

		if not task_list:
			return jsonify({"error": "task list not found"}), 404

		first_incomplete_task = next((task for task in task_list.tasks if not task.completed), None)

		if first_incomplete_task:
			return jsonify({"task": first_incomplete_task.task})
		else:
			return jsonify({"error": "Next task not found"}), 404

	except Exception as e:
		print(f"Error occured: {e}")
		return jsonify({"error": "Internal sever error"}), 500

@tasks_bp.route('/update_task_list', methods=['POST'])
def update_task_list():
	task_list_id = request.json.get('task_list_id')
	print(f"Recieved task list ID: {task_list_id}")
	if task_list_id:
		session['current_task_list_id'] = task_list_id
		return redirect(url_for('tasks.tasks'))
	else:
		return jsonify({"error": "No task list ID provided"}), 400
