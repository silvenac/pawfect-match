from flask import render_template
from flask import request
from app import app
import requests

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        '''
        url = "http://api.petfinder.com/pet.find"
        query_string = {
            "key": "24d0c266ca968b5b62cebb15a71e8693",
            "animal": "dog",
            "format": "json",
            "location": "new york city, ny",
            "count": "25",
            "ouput": "basic"
        }
        response = requests.get(url, params=query_string)
        data = response.json()['petfinder']['pets']['pet'] # array of pets 
        print(data[0])
        '''
        return "hello"
    return render_template('index.html')
