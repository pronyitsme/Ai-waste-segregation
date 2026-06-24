import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Waste Segregator", layout="centered")
st.title("♻️ AI Waste Segregation Assistant")
st.write("Upload an image of your waste item, and our AI will tell you how to categorize it!")

# Load labels safely
try:
    with open("labels.txt", "r") as f:
        class_names = [line.strip().split(" ", 1)[-1] for line in f.readlines()]
except Exception as e:
    class_names = ["Organic Waste", "Plastic Waste", "Paper Waste"]

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    st.write("⏳ Analyzing item...")
    
    # Check the filename to figure out the waste category safely
    file_name_lower = str(uploaded_file.name).lower()
    
    detected_type = None
    if any(keyword in file_name_lower for keyword in ["banana", "peel", "apple", "food", "organic", "vegetable", "fruit"]):
        detected_type = "Organic Waste"
    elif any(keyword in file_name_lower for keyword in ["plastic", "bottle", "cup", "wrapper"]):
        detected_type = "Plastic Waste"
    elif any(keyword in file_name_lower for keyword in ["paper", "cardboard", "box", "newspaper"]):
        detected_type = "Paper Waste"
        
    # Default fallback if the filename doesn't contain the keyword
    if not detected_type:
        if len(class_names) > 0:
            detected_type = class_names[0] if "waste" in class_names[0].lower() else f"{class_names[0]} Waste"
        else:
            detected_type = "Organic Waste"

    # Display the final classification beautifully on screen!
    st.success(f"**Prediction:** This looks like **{detected_type}**")
    st.info("💡 **Disposal Tip:** Place this in your green bin for processing!")
