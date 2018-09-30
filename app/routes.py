from flask import render_template
from flask import request
from app import app
import requests

API_KEY = "111"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = "http://api.petfinder.com/pet.find"
        query_string = {
            "key": API_KEY,
            "animal": "dog",
            "format": "json",
            "location": request.form['location'],
            "sex": request.form['sex'],
            "age": request.form['age'],
            "size": request.form['size'],
            "count": "25",
            "output": "basic"
        }
        response = requests.get(url, params=query_string)
        data = response.json()['petfinder']['pets']['pet'] # array of pets 
        url_dict = {}
        for i in range(len(data)):
            try:
                url_dict[data[i]['id']['$t']] = data[i]['media']['photos']['photo'][0]['$t']
            except:
                print(i)
        print(url_dict)
        return "hello"
    return render_template('index.html')
