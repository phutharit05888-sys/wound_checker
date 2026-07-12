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
    return tf.keras.models.load_model("dfu_final_model (3).keras")

model = load_model()

# =========================
# Image Size
# =========================
IMG_SIZE = 260

# =========================
# Streamlit UI
# =========================
st.set_page_config(
    page_title="วิเคราะห์และคัดกรองความเสี่ยงของแผล",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 วิเคราะห์และคัดกรองความเสี่ยงของแผล")

st.markdown("""
อัปโหลดหรือถ่ายภาพแผลที่เท้าของผู้ป่วยเพื่อนำไปวิเคราะห์ด้วย AI
""")

# =========================
# Image Source
# =========================

st.subheader("เลือกวิธีอัปโหลดรูปภาพ")

tab1, tab2 = st.tabs([
    "📁 อัปโหลดรูปภาพ",
    "📷 กล้องถ่าย"
])

image = None

with tab1:

    uploaded_file = st.file_uploader(
        "อัปโหลดรูปภาพ",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

with tab2:

    camera_photo = st.camera_input(
        "ถ่ายภาพแผล"
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

    with st.spinner("วิเคราะห์รูปภาพ..."):

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

    st.subheader("ผลประเมิน")

    if predicted_class == "Grade 1":

        st.success(f"🟢 {predicted_class}")
        st.info("มีความเสี่ยงจะเกิดแผล ควรดูแลและเฝ้าระวังอย่างเหมาะสม")

    elif predicted_class == "Grade 2":

        st.warning(f"🟡 {predicted_class}")
        st.info("ควรพบแพทย์เพื่อเข้ารับการรักษาก่อนที่บาดแผลเกิดการลุกลาม")

    elif predicted_class == "Grade 3":

        st.warning(f"🟠 {predicted_class}")
        st.info("ควรพบแพทย์โดยด่วน เนื่องจากบาดแผลมีความเสี่ยงรุนแรงที่จะเกิดเนื้อตาย ซึ่งอาจนำไปสู่การตัดอวัยวะ")

    else:

        st.error(f"🔴 {predicted_class}")
        st.error("ควรพบแพทย์โดยด่วน เนื่องจากบาดแผลมีความเสี่ยงรุนแรงที่จะเกิดเนื้อตาย ซึ่งอาจนำไปสู่การตัดอวัยวะ")

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    # =========================
    # Recommendation
    # =========================

    st.divider()

    st.subheader("คำแนะนำการดูแลแผลเบื้องต้น")

    if predicted_class == "Grade 1":

        st.success("""
• มีความเสี่ยงจะเกิดแผล

• ควรดูแลและเฝ้าระวังอย่างเหมาะสม
""")

    elif predicted_class == "Grade 2":

        st.warning("""
• ควรพบแพทย์เพื่อเข้ารับการรักษาก่อนที่บาดแผลเกิดการลุกลาม
""")

    elif predicted_class == "Grade 3":

        st.warning("""
• ควรพบแพทย์โดยด่วน เนื่องจากบาดแผลมีความเสี่ยงรุนแรงที่จะเกิดเนื้อตาย ซึ่งอาจน าไปสู่การตัด
อวัยวะ
""")

    else:

        st.error("""
• ควรพบแพทย์โดยด่วน เนื่องจากบาดแผลมีความเสี่ยงรุนแรงที่จะเกิดเนื้อตาย ซึ่งอาจน าไปสู่การตัด
อวัยวะ
""")

    # =========================
    # Medical Disclaimer
    # =========================

    st.divider()

    st.caption(
        "⚠️ This AI system is intended for screening purposes only. "
        "It does not replace diagnosis or treatment by a qualified healthcare professional."
    )
