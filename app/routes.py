from flask import render_template
from flask import request
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		return "Made post request"
	return render_template('index.html')