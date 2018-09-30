from flask import render_template
from flask import request, session, redirect, url_for, flash
from app import app
import requests
from PIL import Image
from io import BytesIO
from keras.preprocessing import image
from keras.applications.mobilenet import MobileNet, preprocess_input
from .vectorize import get_vectors, get_vector
from .knn import build_tree, query
import string
import re

global model

model = MobileNet(input_shape=(224,224,3), include_top=False, weights='imagenet', pooling='avg')

API_KEY = "24d0c266ca968b5b62cebb15a71e8693"

if 'model' not in globals():
    print('yikes')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
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
        try:
            data = response.json()['petfinder']['pets']['pet'] # array of pets
        except KeyError:
            return "No Results Found"

        url_dict = {}
        for i in range(len(data)):
            try:
                url_dict[data[i]['id']['$t']] = data[i]['media']['photos']['photo'][3]['$t']
            except:
                print(i)

        dog_img = request.files['doggo'].read()
        temp = Image.open(BytesIO(dog_img))
        img = temp.copy().resize((224,224))
        # temp.close()
        petfinder_vector = get_vectors(url_dict, model)
        user_img = get_vector(img, model)
        # print(petfinder_vector, user_img)
        tree, index_to_id = build_tree(petfinder_vector)
        most_similar_dogs = query(user_img, 5, tree, index_to_id)
        print(most_similar_dogs)
        session['most_similar_dogs'] = most_similar_dogs
        return redirect(url_for('mydoggos'))
    return render_template('index.html')

@app.route('/mydoggos', methods=['GET', 'POST'])
def mydoggos():

    url = "http://api.petfinder.com/pet.get"
    base_url = "http://www.petfinder.com/dog"

    dog_list = [] #[[dog_name, photo, url], [...], ...]


    id_list = session.get('most_similar_dogs', None)

    for id in id_list:
        query_string = {
            "key": API_KEY,
            "format": "json",
            "id": id
        }

        response = requests.get(url, params=query_string).json()
        if(response['petfinder'].get('header')):
                continue
        try:
            # get info from JSON object returned by API
            data = response['petfinder']['pet'] # array of pets
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

        except KeyError as e:
            print(e)
            flash('No matches, please try again!')
            return redirect(url_for('index'))

        except Exception as e:
            print("Error", e)

        this_url = base_url + '/' + no_punct_dog_name + '-' + dog_id + '/' + \
                no_punct_state + '/' + no_punct_city + '/' + no_punct_shelter_name + \
                '-' + str(shelter_id)
        this_url = this_url.lower()

        this_list = [dog_name, photo, this_url]
        dog_list.append(this_list)

    return render_template('mydoggos.html', list=dog_list)
