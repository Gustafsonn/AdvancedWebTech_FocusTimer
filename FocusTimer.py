from flask import Flask, render_template
app = Flask(__name__)

@app.route('/Home/')
def Home():
	return render_template('Base.html')

if __name__ == ("__main__"):
	app.run(host='0.0.0.0', debug=True)
