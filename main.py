import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import io
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

from flask import Flask, request, jsonify

# Use raw string for the file path
model_path = r"D:\End to End Mlops using GCP\End-to-End-MLOps-Project-with-GCP\nn.h5"
# Check if the file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"The file {model_path} does not exist.")
else:
    print(f"The file {model_path} exists.")

# Load model architecture and weights separately
model = keras.models.load_model(model_path, compile=False)

# Compile the model manually
model.compile(
    optimizer=keras.optimizers.Adam(),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

def transform_image(pillow_image):
    data = np.asarray(pillow_image)
    data = data / 255.0
    data = data[np.newaxis, ..., np.newaxis]
    data = tf.image.resize(data, [28, 28])
    return data

def predict(x):
    predictions = model(x)
    predictions = tf.nn.softmax(predictions)
    pred0 = predictions[0]
    label0 = np.argmax(pred0)
    return label0

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes)).convert('L')
            tensor = transform_image(pillow_img)
            prediction = predict(tensor)
            data = {"prediction": int(prediction)}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
