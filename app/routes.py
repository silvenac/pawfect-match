from flask import render_template
from flask import request
from app import app
import requests
import string
import re

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        '''
        url = "http://api.petfinder.com/pet.find"
        query_string = {
            "key": "API_KEY",
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

@app.route('/mydoggos', methods=['GET', 'POST'])
def mydoggos():
API_KEY = '24d0c266ca968b5b62cebb15a71e8693'
url = "http://api.petfinder.com/pet.get"
base_url = "http://www.petfinder.com/dog"

dog_list = [] #[[dog_name, photo, url], [...], ...]

id_list=[36974356] #TODO PLACEHOLDER FOR REAL LIST
for id in id_list:
    query_string = {
        "key": API_KEY,
        "format": "json",
        "id": id
    }
    response = requests.get(url, params=query_string)
    try:
        # get info from JSON object returned by API
        data = response.json()['petfinder']['pet'] # array of pets
        dog_name = data['name']['$t']
        dog_id = data['id']['$t']
        state = data['contact']['state']['$t']
        city = data['contact']['city']['$t']
        shelter_id = data['shelterId']['$t']
        photo = data['media']['photos']['photo'][0]['$t']

        url = "http://api.petfinder.com/shelter.get"
        shelter_query = {"key":"24d0c266ca968b5b62cebb15a71e8693",
               "format":"json","id": shelter_id}
        shelt = requests.get(url, params=shelter_query)
        shelt_json = shelt.json()
        shelter_name = shelt_json['petfinder']['shelter']['name']['$t']

        translator = str.maketrans('', '', string.punctuation)
        no_punct_dog_name = dog_name.replace("&", "and")
        no_punct_dog_name = dog_name.translate(translator)
        no_punct_dog_name =  re.sub(' +', ' ', no_punct_dog_name)
        no_punct_dog_name = no_punct_dog_name.replace(' ', '-')

        no_punct_state = state.replace(' ', '-')

        translator = str.maketrans('', '', string.punctuation)
        no_punct_city = city.replace("&", "and")
        no_punct_city = city.translate(translator)
        no_punct_city =  re.sub(' +', ' ', no_punct_city)
        no_punct_city = no_punct_city.replace(' ', '-')

        no_punct_shelter_name = shelter_name.replace('&', 'and')
        no_punct_shelter_name = no_punct_shelter_name.translate(translator)
        no_punct_shelter_name =  re.sub(' +', ' ', no_punct_shelter_name)
        no_punct_shelter_name = no_punct_shelter_name.replace(' ', '-')

    except:
        print("Error")

    this_url = base_url + '/' + no_punct_dog_name + '-' + dog_id + '/' + \
            no_punct_state + '/' + no_punct_city + '/' + no_punct_shelter_name + \
            '-' + str(shelter_id)
    this_url = this_url.lower()

    this_list = [dog_name, photo, this_url]
    dog_list.append(this_list)

    return render_template('mydoggos.html', list=dog_list)
