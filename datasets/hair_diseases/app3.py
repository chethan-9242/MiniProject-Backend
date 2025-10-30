import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from keras.models import load_model

# Load the trained InceptionV3 model
model = load_model('2_InceptionV3.h5')

# Define class names (you can fetch these from your training data directory)
# Define class names
class_names = [
    "Alopecia Areata",
    "Contact Dermatitis",
    "Folliculitis",
    "Head Lice",
    "Lichen Planus",
    "Male Pattern Baldness",
    "Psoriasis",
    "Seborrheic Dermatitis",
    "Telogen Effluvium",
    "Tinea Capitis",
]

st.title("Hair Disease Classification")

# Upload an image for classification
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    # Display the uploaded image
    st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

    # Preprocess the image for model prediction
    img = Image.open(uploaded_image)
    img = img.resize((299, 299))  # Resize image to match model's expected sizing
    img = np.asarray(img)
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Make predictions
    predictions = model.predict(img)

    # Display the class with the highest probability
    max_prob_class_index = np.argmax(predictions)
    st.subheader("Prediction:")
    st.write(f"Class: {class_names[max_prob_class_index]}")

    # Display class probabilities
    st.subheader("Class Probabilities:")
    for i, class_name in enumerate(class_names):
        st.write(f"{class_name}: {predictions[0][i]:.4f}")
