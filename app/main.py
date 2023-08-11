import logging
import os

from flask import Flask, render_template, request
import google.cloud.logging
from google.cloud import firestore
from google.cloud import storage

client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    
    # Inicializa el cliente de la API Cloud Vision
    client = vision.ImageAnnotatorClient()

    content = image.read()
    image = vision.Image(content=content)

    # Realiza la detección de celebridades
    response = client.face_detection(image=image)
    faces = response.face_annotations

    return render_template('result.html', faces=faces)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return render_template('error.html'), 500

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))

