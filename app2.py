import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import os

from datetime import datetime
from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="ระบบวิเคราะห์และคัดกรองความเสี่ยงของแผล",
    page_icon="🩺",
    layout="centered"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp{
    background:#EAF4FF;
}

.block-container{
    max-width:900px;
    padding-top:20px;
}

.title{
    color:#11468F;
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    color:#4D4D4D;
    font-size:18px;
}

.upload-card{
    background:#D5ECFF;
    border:5px solid #5B86E5;
    border-radius:25px;
    padding:35px;
    text-align:center;
    margin-top:20px;
    margin-bottom:25px;
}

.upload-card h2{
    color:#11468F;
}

.stButton>button{
    width:100%;
    border-radius:12px;
    height:55px;
    font-size:18px;
    font-weight:bold;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:15px;
    border:2px solid #d9d9d9;
}

.result-card{
    background:white;
    padding:20px;
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# MODEL
# ==========================================

classes = [
    "Grade 1",
    "Grade 2",
    "Grade 3",
    "Grade 4"
]

IMG_SIZE = 260


@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "dfu_final_model (3).keras"
    )


model = load_model()

# ==========================================
# HEADER
# ==========================================

left,right = st.columns([8,1])

with left:
    st.markdown(
        '<div class="title">🩺 วิเคราะห์และคัดกรองความเสี่ยงของแผล</div>',
        unsafe_allow_html=True
    )

with right:
    st.markdown("# 👤")

st.markdown(
"""
<div class="subtitle">

อัปโหลดหรือถ่ายภาพแผลของผู้ป่วยเพื่อให้ระบบ AI วิเคราะห์ระดับความเสี่ยง

</div>
""",
unsafe_allow_html=True
)

# ==========================================
# MAIN CARD
# ==========================================

st.markdown("""
<div class="upload-card">

# 📷

## เริ่มการประเมินแผล

เลือกวิธีการนำเข้ารูปภาพด้านล่าง

</div>
""",
unsafe_allow_html=True)

tab1, tab2 = st.tabs([
    "📁 อัปโหลดรูปภาพ",
    "📷 ถ่ายภาพจากกล้อง"
])

image = None

with tab1:

    uploaded_file = st.file_uploader(
        "เลือกรูปภาพ",
        type=["jpg","jpeg","png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

with tab2:

    camera_photo = st.camera_input(
        "เปิดกล้อง"
    )

    if camera_photo is not None:
        image = Image.open(camera_photo).convert("RGB")

# ==========================================
# IMAGE PREVIEW
# ==========================================

if image is not None:

    st.image(
        image,
        caption="ภาพที่เลือก",
        use_container_width=True
    )

    img = image.resize((IMG_SIZE, IMG_SIZE))

    image_array = np.array(
        img,
        dtype=np.float32
    )

    image_array = preprocess_input(
        image_array
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    with st.spinner("AI กำลังวิเคราะห์ภาพ..."):

        prediction = model.predict(
            image_array,
            verbose=0
        )

    predicted_index = np.argmax(prediction)

    confidence = float(
        np.max(prediction) * 100
    )

    predicted_class = classes[predicted_index]

st.markdown("""
<style>

.stApp{
    background:#EAF4FF;
}

.block-container{
    max-width:900px;
    padding-top:20px;
}

.title{
    color:#11468F;
    font-size:38px;
    font-weight:bold;
}

.subtitle{
    color:#555555;
    font-size:18px;
    margin-bottom:15px;
}

.upload-card{
    background:#CFE8FF;
    border:5px solid #4F7DDA;
    border-radius:30px;
    padding:40px;
    text-align:center;
    margin-top:20px;
    margin-bottom:30px;
}

.upload-card h2{
    color:#11468F;
}

.upload-card p{
    color:#444444;
    font-size:18px;
}

.result-card{
    background:white;
    border-radius:20px;
    padding:20px;
    border:1px solid #D8D8D8;
}

.stButton>button{
    width:100%;
    border-radius:15px;
    height:55px;
    font-size:18px;
    font-weight:bold;
    background:#6DAEFF;
    color:white;
}

.stButton>button:hover{
    background:#5A9AF5;
    color:white;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    border:2px solid #E0E0E0;
    padding:15px;
}

hr{
    border:1px solid #BFD8FF;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# CLASSES
# ==========================================

classes = [
    "Grade 1",
    "Grade 2",
    "Grade 3",
    "Grade 4"
]

IMG_SIZE = 260

# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("dfu_final_model (3).keras")

model = load_model()

# ==========================================
# HEADER
# ==========================================

left, right = st.columns([8,1])

with left:
    st.markdown(
        '<div class="title">🏥 วิเคราะห์และคัดกรองความเสี่ยงของแผล</div>',
        unsafe_allow_html=True
    )

with right:
    st.markdown("## 👤")

st.markdown(
"""
<div class="subtitle">
อัปโหลดหรือถ่ายภาพแผลที่เท้าของผู้ป่วย เพื่อให้ระบบ AI วิเคราะห์ระดับความรุนแรงของแผลเบาหวาน
</div>
""",
unsafe_allow_html=True
)

# ==========================================
# MAIN CARD
# ==========================================

st.markdown("""
<div class="upload-card">

# 📷

## เริ่มการประเมินแผล

เลือกวิธีการนำเข้ารูปภาพด้านล่าง

</div>
""",
unsafe_allow_html=True)

tab1, tab2 = st.tabs([
    "📁 อัปโหลดรูปภาพ",
    "📷 ถ่ายภาพจากกล้อง"
])

image = None

with tab1:

    uploaded_file = st.file_uploader(
        "เลือกรูปภาพ",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")

with tab2:

    camera_photo = st.camera_input(
        "เปิดกล้อง"
    )

    if camera_photo is not None:
        image = Image.open(camera_photo).convert("RGB")

# ==========================================
# IMAGE PREVIEW & PREPROCESS
# ==========================================

if image is not None:

    st.image(
        image,
        caption="ภาพที่เลือก",
        use_container_width=True
    )

    img = image.resize((IMG_SIZE, IMG_SIZE))

    image_array = np.array(
        img,
        dtype=np.float32
    )

    image_array = preprocess_input(
        image_array
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    with st.spinner("🤖 AI กำลังวิเคราะห์ภาพ..."):

        prediction = model.predict(
            image_array,
            verbose=0
        )

    predicted_index = np.argmax(prediction)
    confidence = float(np.max(prediction) * 100)
    predicted_class = classes[predicted_index]
