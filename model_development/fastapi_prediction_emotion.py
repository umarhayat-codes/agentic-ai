

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image
import base64

app = FastAPI()

# Load facial emotion model
model = load_model("facial_emotion_model.keras")

# Define class names according to your training labels
class_names = ['angry', 'happy']

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read uploaded image
    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")
    img = img.resize((150, 150))  # Resize to match model input size

    # Convert image to array
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Make prediction
    prediction = model.predict(img_array)
    predicted_class = class_names[int(prediction[0][0] > 0.5)]  # 0 or 1

    # Optional: Convert image to base64 for visualization/debugging
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return JSONResponse(content={
        "prediction": predicted_class,
        # "image_base64": img_base64  # Uncomment if you want to return the image too
    })
