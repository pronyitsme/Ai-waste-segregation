import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Waste Segregator", layout="centered")
st.title("♻️ AI Waste Segregation Assistant")
st.write("Upload an image of your waste item, and our AI will tell you how to categorize it!")

# Load labels safely
try:
    with open("labels.txt", "r") as f:
        # This reads your categories smoothly
        class_names = [line.strip().split(" ", 1)[-1] for line in f.readlines()]
except Exception as e:
    st.error("Could not load labels.txt file. Make sure it is in your repository.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)
    st.success("🎉 Image uploaded successfully!")
    if 'class_names' in locals():
        st.info(f"🔮 The model will check for these categories: {', '.join(class_names)}")
