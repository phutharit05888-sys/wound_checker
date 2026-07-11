import streamlit as st
import tensorflow as tf
import numpy as np

from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input

# =========================
# Classes
# =========================
classes = [
    "Grade 1",
    "Grade 2",
    "Grade 3",
    "Grade 4"
]

# =========================
# Load Model
# =========================
model = tf.keras.models.load_model("best_dfu_model.keras")

# =========================
# Image Size
# =========================
IMG_SIZE = 260

# =========================
# Streamlit UI
# =========================
st.set_page_config(
    page_title="AI Diabetic Foot Ulcer Detection",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 AI Diabetic Foot Ulcer Detection System")

st.write(
    """
    Upload an image of a diabetic foot ulcer for AI analysis.

    The AI model will classify the wound into one of four severity grades.
    """
)

st.subheader("Select Image Source")

tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Camera"])

image = None

with tab1:
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

with tab2:
    camera_image = st.camera_input("Take a picture of the wound")

    if camera_image is not None:
        image = Image.open(camera_image).convert("RGB")

# =========================
# Prediction
# =========================
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    # Preprocess Image
    image = image.resize((IMG_SIZE, IMG_SIZE))

    image_array = np.array(image, dtype=np.float32)

    image_array = preprocess_input(image_array)

    image_array = np.expand_dims(image_array, axis=0)

    # Predict
    prediction = model.predict(image_array)

    predicted_index = np.argmax(prediction)

    confidence = np.max(prediction) * 100

    predicted_class = classes[predicted_index]

    # =========================
    # Output
    # =========================
    st.subheader("Prediction Result")

    if predicted_class == "Grade 1":
        st.success(f"🟢 {predicted_class}")
        st.info("Low Severity")

    elif predicted_class == "Grade 2":
        st.warning(f"🟡 {predicted_class}")
        st.info("Moderate Severity")

    elif predicted_class == "Grade 3":
        st.warning(f"🟠 {predicted_class}")
        st.info("High Severity")

    else:
        st.error(f"🔴 {predicted_class}")
        st.error("Critical Severity")

    st.write(f"### Confidence: {confidence:.2f}%")

    st.subheader("AI Recommendation")

    if predicted_class == "Grade 1":
        st.write(
            "• Continue daily wound care.\n"
            "• Keep the wound clean.\n"
            "• Monitor for any signs of infection."
        )

    elif predicted_class == "Grade 2":
        st.write(
            "• Clean the wound regularly.\n"
            "• Reduce pressure on the affected foot.\n"
            "• Consider consulting a healthcare professional."
        )

    elif predicted_class == "Grade 3":
        st.write(
            "• Seek medical attention as soon as possible.\n"
            "• Avoid walking on the affected foot.\n"
            "• Follow professional wound care instructions."
        )

    else:
        st.write(
            "• Immediate medical attention is strongly recommended.\n"
            "• Do not delay treatment.\n"
            "• Visit a hospital or wound care specialist immediately."
        )
