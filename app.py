import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf

st.set_page_config(page_title="AI Waste Segregator", layout="centered")
st.title("♻️ AI Waste Segregation Assistant")
st.write("Upload an image of your waste item, and our AI will tell you how to categorize it!")

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("keras_model.h5", compile=False)
    with open("labels.txt", "r") as f:
        class_names = [line.strip() for line in f.readlines()]
    return model, class_names

try:
    model, class_names = load_model()
except Exception as e:
    st.error("Error loading model files.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    st.write("⏳ Analyzing item...")
    
    size = (224, 224)
    image_resized = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image_resized)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    
    st.success(f"**Prediction:** This looks like **{class_name[2:]}**")
    st.info(f"**Confidence Level:** {float(confidence_score) * 100:.2f}%")
