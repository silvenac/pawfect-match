import requests
from PIL import Image
from keras.preprocessing import image
from keras.applications.mobilenet import MobileNet, preprocess_input
from io import BytesIO
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

global model

def get_images(url_dict):
    def get(url):
        response = requests.get(url)
        temp = Image.open(BytesIO(response.content))
        img = temp.copy().resize((224,224))
        temp.close()
        return img

    results = dict()
    with ThreadPoolExecutor(5) as executor:
        future_to_id = {executor.submit(get, url): key for key, url in url_dict.items()}
        for future in as_completed(future_to_id):
            unique_id = future_to_id[future]
            try:
                img = future.result()
                results[unique_id] = img
            except Exception as e:
                print(e)
    return results

def get_vectors(url_dict, model):
    image_dict = get_images(url_dict)
    results = dict()
    for unique_id, img in image_dict.items():
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        vector = model.predict(x)
        results[unique_id] = vector
    return results

def get_vector(img, model):
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return model.predict(x)
