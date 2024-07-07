import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import io
import tensorflow as tf
from tensorflow import keras    
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify

model = keras.models.load_model('nn.h5')

def transform_image(pillow_image):
    data = np.asarray(pillow_image)
    data = data / 255.0
    data = data[np.newaxis, ..., np.newaxis]
    data = tf.image.resize(data, [28, 28])
    return data

def predict(image):
    predictions = model(x)
    predictions = tf.nn.softmax(predictions)
    pred0 = predictions[0]
    label0 = np.argmax(pred0)
    return label0

app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
