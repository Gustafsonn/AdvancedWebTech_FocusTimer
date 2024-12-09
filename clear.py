from app import create_app, db
from app.models import TaskList, User

app = create_app()

with app.app_context():
	TaskList.query.delete()
	User.query.delete()
	db.session.commit()

	print("data cleared")
