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
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("best_dfu_model.keras")

model = load_model()

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

st.markdown("""
Upload or capture an image of a diabetic foot ulcer for AI analysis.

The AI model will classify the wound into one of four severity grades.
""")

# =========================
# Image Source
# =========================

st.subheader("Choose Image Source")

tab1, tab2 = st.tabs([
    "📁 Upload Image",
    "📷 Camera"
])

image = None

with tab1:

    uploaded_file = st.file_uploader(
        "Upload a wound image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

with tab2:

    camera_photo = st.camera_input(
        "Take a picture"
    )

    if camera_photo is not None:
        image = Image.open(camera_photo).convert("RGB")

# =========================
# Prediction
# =========================

if image is not None:

    st.image(
        image,
        caption="Selected Image",
        use_container_width=True
    )

    img = image.resize((IMG_SIZE, IMG_SIZE))

    image_array = np.array(
        img,
        dtype=np.float32
    )

    image_array = preprocess_input(image_array)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    with st.spinner("Analyzing image..."):

        prediction = model.predict(
            image_array,
            verbose=0
        )

    predicted_index = np.argmax(prediction)

    confidence = float(np.max(prediction) * 100)

    predicted_class = classes[predicted_index]

    # =========================
    # Results
    # =========================

    st.divider()

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

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    # =========================
    # Recommendation
    # =========================

    st.divider()

    st.subheader("AI Recommendation")

    if predicted_class == "Grade 1":

        st.success("""
• Continue daily wound care.

• Keep the wound clean.

• Monitor for any signs of infection.

• Continue regular follow-up if needed.
""")

    elif predicted_class == "Grade 2":

        st.warning("""
• Clean the wound regularly.

• Reduce pressure on the affected foot.

• Schedule an appointment with a healthcare professional.

• Monitor the wound every day.
""")

    elif predicted_class == "Grade 3":

        st.warning("""
• Seek medical attention as soon as possible.

• Avoid walking on the affected foot.

• Follow professional wound care instructions.

• Infection risk may be increased.
""")

    else:

        st.error("""
• Immediate medical attention is strongly recommended.

• Do not delay treatment.

• Visit a hospital or wound care specialist immediately.

• Emergency wound management may be required.
""")

    # =========================
    # Medical Disclaimer
    # =========================

    st.divider()

    st.caption(
        "⚠️ This AI system is intended for screening purposes only. "
        "It does not replace diagnosis or treatment by a qualified healthcare professional."
    )
