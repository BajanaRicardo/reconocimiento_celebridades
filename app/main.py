import logging
import os

from flask import Flask, render_template, request
import google.cloud.logging
from google.cloud import firestore
from google.cloud import storage
from google.cloud import vision

client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()
vision_client = vision.ImageAnnotatorClient()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    successful_upload = False
    if request.method == 'POST':
        uploaded_file = request.files.get('picture')

        if uploaded_file:
            gcs = storage.Client()
            bucket = gcs.get_bucket(os.environ.get('BUCKET', 'my-bmd-bucket'))
            blob = bucket.blob(uploaded_file.filename)

            blob.upload_from_string(
                uploaded_file.read(),
                content_type=uploaded_file.content_type
            )

            celebrities = []

            # Realizar el reconocimiento de famosos utilizando Google Vision AI
            image = vision.Image(content=uploaded_file.read())
            response = vision_client.face_detection(image=image)

            for face in response.face_annotations:
                for celebrity in face.recognized_celebrity:
                    celebrities.append(celebrity.name)
            return render_template('result.html', successful_upload=True, celebrities=celebrities)
        return render_template('index.html', successful_upload=False)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return render_template('error.html'), 500

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))

