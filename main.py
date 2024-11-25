# %%
from typing import Union
from fastapi import FastAPI
import fastapi
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from fastapi.responses import JSONResponse
from PIL import Image
import io
from fastapi import HTTPException
import requests
from io import BytesIO
from pydantic import BaseModel

app = FastAPI()

import h5py

#Define la ruta correcta al archivp
file_path = './MODELO.h5'
#H
model = load_model(file_path, compile=False)

#Abre el archivo
with h5py.File(file_path, 'r') as f:
     Realiza operaciones con el archivo
    print(list(f.keys()))  # Por ejemplo, imprimir las claves del archivo

#Definir las clases
class_names = ['Normal', 'Anomalía']  # Cambia según tu contexto

class ImageURL(BaseModel):
    url: str

def preprocess_image(image):
     #Redimensionar la imagen a 256x256
    image = image.resize((256, 256))

     #Convertir la imagen a RGB (asegúrate de que tenga 3 canales)
    image = image.convert("RGB")

     #Convertir a un array de NumPy
    image_array = np.array(image)

     #Agregar una dimensión para el batch
    image_array = np.expand_dims(image_array, axis=0)  # Ahora tiene forma (1, 256, 256, 3)

     #Normalizar el array
    return image_array.astype('float32') / 255.0  # Normalizar a [0, 1]
import requests

@app.post("/analyze_image/")
async def analyze_image(image: ImageURL):
    try:
         #Agrega un tiempo de espera
        response = requests.get(image.url, timeout=10)  # Tiempo de espera de 10 segundos
        if response.status_code != 200:
            #raise HTTPException(status_code=400, detail="No se pudo descargar la imagen")

        #Abrir la imagen y preprocesarla
       img = Image.open(BytesIO(response.content))
        processed_image = preprocess_image(img)

        #Realizar la predicción
        prediction = model.predict(processed_image)
        predicted_class_index = np.argmax(prediction, axis=-1)[0]
        predicted_class = class_names[predicted_class_index]

       return {
            "filename": "remote_image",
            "message": "Image processed and analyzed.",
           "prediction": predicted_class
        }
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Timeout: La URL tardó demasiado en responder")
    except Exception as e:
     #  raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {str(e)}")

@app.get("/tf_version/")
def tf_version():
    return tf.__version__

#python3 -m uvicorn FastAPI:app --reload --port 8007