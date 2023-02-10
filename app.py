import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import threading
from pyngrok import ngrok

import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten, Conv2D, Dropout, MaxPool2D
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import pandas as pd
import os
import math

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = '/content/drive/MyDrive/FlaskProject/Uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
port = 5000

# Open a ngrok tunnel to the HTTP server
NGROK_AUTH_TOKEN="2LB1PwM7VocOi2c6j6ve33uQn3A_2nde4GiBiJ2GwzVB65PXe"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(port,"http",remote_addr="http://127.0.0.1:3000").public_url

print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url
# app.config['DEBUG'] = True


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, support_credentials=True)

@app.route("/")
def hello_world():
    return {"message":"hello world"}




@app.route('/predict', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'.')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file']
    
    model = request.form.get('model')
    model = "custom_CNN" if model == "Custom" else "transfer_vgg19"
    
    
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    model = tf.keras.models.load_model('/content/drive/MyDrive/Models/saved_models/'+model +'.h5')
    img = image.load_img(UPLOAD_FOLDER+"/"+file.filename,target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array,axis=0)
    img_preprocessed = preprocess_input(img_batch)
    prediction = model.predict(img_batch)
    
    a=np.argmax(prediction,axis=1)
    response="Infected" if a==0 else "Uninfected"
 
    
    return {"result": response}

if __name__ == '__main__':
    app.run()



