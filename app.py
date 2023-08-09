from flask import Flask, render_template, request
from google.cloud import vision

app = Flask(__name__)

# Configura las credenciales de la API Cloud Vision (reemplaza 'ruta/a/tu/credencial.json' con la ubicación de tus propias credenciales)
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ruta/a/tu/credencial.json'

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

if __name__ == '__main__':
    app.run(debug=True)
