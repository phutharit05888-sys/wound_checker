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

st.markdown(<style>

.main{
    background:#EEF5FF;
}

.block-container{
    padding-top:1rem;
    max-width:700px;
}

.title{
    color:#0F3F87;
    font-size:34px;
    font-weight:bold;
}

.upload-box{
    border:6px solid #4D74B8;
    border-radius:25px;
    background:#CFE8FF;
    padding:40px;
    text-align:center;
    margin-top:30px;
    margin-bottom:40px;
}

.menu-button{
    background:#8EC5FF;
    border-radius:20px;
    text-align:center;
    padding:25px;
    font-size:22px;
    font-weight:bold;
}

hr{
    border:1px solid #4066A8;
}

</style>
""", unsafe_allow_html=True)

col1,col2 = st.columns([8,1])

with col1:
    st.markdown('<div class="title">🏥 หน้าหลัก</div>',unsafe_allow_html=True)

with col2:
    st.markdown("# 👤")

st.markdown("""
<div class="upload-box">

# 📷

### เริ่มการประเมินแผล

</div>
""",unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["jpg","jpeg","png"],
    label_visibility="collapsed"
)

camera = st.camera_input(
    "",
    label_visibility="collapsed"
)

st.divider()

col1,col2 = st.columns(2)

with col1:

    st.button(
        "🏠 หน้าแรก",
        use_container_width=True
    )

with col2:

    st.button(
        "📄 ประวัติการประเมิน",
        use_container_width=True
    )

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
