import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import os

from datetime import datetime
from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="วิเคราะห์และคัดกรองความเสี่ยงของแผล",
    page_icon="🩺",
    layout="centered"
)

# =====================================================
# CUSTOM STYLE
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#EEF7FF;
}

.block-container{
    max-width:900px;
    padding-top:30px;
}

.title{
    font-size:38px;
    font-weight:bold;
    color:#11468F;
}

.subtitle{
    color:#666;
    font-size:18px;
}

.card{

    background:white;

    padding:25px;

    border-radius:25px;

    box-shadow:0 4px 12px rgba(0,0,0,.08);

    margin-top:20px;

}

.result-card{

    background:white;

    border-radius:20px;

    padding:20px;

    border:1px solid #E0E0E0;

}

.footer{

    color:gray;

    font-size:14px;

    text-align:center;

}

.stButton>button{

    width:100%;

    border-radius:15px;

    height:52px;

    font-size:17px;

    font-weight:bold;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# MODEL
# =====================================================

CLASSES = [
    "Grade 1",
    "Grade 2",
    "Grade 3",
    "Grade 4"
]

IMG_SIZE = 128

MODEL_PATH = "dfu_final_model (5).keras"

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

model = load_model()

# =====================================================
# HISTORY FILE
# =====================================================

HISTORY_FILE = "assessment_history.csv"

if not os.path.exists(HISTORY_FILE):

    history = pd.DataFrame(columns=[
        "วันที่และเวลา",
        "ผลการประเมิน",
        "Confidence",
        "คำแนะนำ"
    ])

    history.to_csv(
        HISTORY_FILE,
        index=False,
        encoding="utf-8-sig"
    )

# =====================================================
# HEADER
# =====================================================

st.markdown(
"""
<div class="title">
🩺 วิเคราะห์และคัดกรองความเสี่ยงของแผล
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">

อัปโหลดหรือถ่ายภาพแผลที่เท้าของผู้ป่วย
เพื่อให้ AI วิเคราะห์ระดับความรุนแรงของแผล

</div>
""",
unsafe_allow_html=True
)

# =====================================================
# UPLOAD CARD
# =====================================================

with st.container(border=True):

    st.subheader("📷 เลือกวิธีการประเมิน")

    tab1, tab2 = st.tabs([
        "📁 อัปโหลดรูปภาพ",
        "📷 ถ่ายภาพ"
    ])

    image = None

    with tab1:

        uploaded_file = st.file_uploader(
            "เลือกรูปภาพ",
            type=["jpg","jpeg","png"]
        )

        if uploaded_file is not None:

            image = Image.open(
                uploaded_file
            ).convert("RGB")

    with tab2:

        camera_photo = st.camera_input(
            "ถ่ายภาพแผล"
        )

        if camera_photo is not None:

            image = Image.open(
                camera_photo
            ).convert("RGB")

# =====================================================
# AI PREDICTION
# =====================================================

if image is not None:

    st.image(
        image,
        caption="ภาพที่เลือก",
        use_container_width=True
    )

    img = image.resize(
        (IMG_SIZE, IMG_SIZE)
    )

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

    with st.spinner("🤖 AI กำลังวิเคราะห์..."):

        prediction = model.predict(
            image_array,
            verbose=0
    )

    predicted_index = np.argmax(prediction)

    confidence = float(
        np.max(prediction) * 100
    )

    predicted_class = CLASSES[predicted_index]

    # =====================================================
    # RESULT TEXT
    # =====================================================

    if predicted_class == "Grade 1":

        risk_text = "มีความเสี่ยงจะเกิดแผล"

        recommendation = """
ควรล้างแผลด้วยน้ำเกลือปราศจากเชื้อ

ทำความสะอาดแผลทุกวัน

หลีกเลี่ยงการกดทับบริเวณแผล

ติดตามอาการอย่างสม่ำเสมอ
"""

        color = "🟢"

    elif predicted_class == "Grade 2":

        risk_text = "ควรพบแพทย์"

        recommendation = """
ควรเข้ารับการรักษา

ทำแผลอย่างถูกวิธี

ลดการลงน้ำหนักที่เท้า

ปฏิบัติตามคำแนะนำของแพทย์
"""

        color = "🟡"

    elif predicted_class == "Grade 3":

        risk_text = "ควรพบแพทย์โดยด่วน"

        recommendation = """
แผลมีความเสี่ยงรุนแรง

ควรพบแพทย์โดยเร็วที่สุด

หลีกเลี่ยงการเดิน

ดูแลแผลให้สะอาด
"""

        color = "🟠"

    else:

        risk_text = "ควรพบแพทย์โดยด่วน"

        recommendation = """
แผลอยู่ในระดับวิกฤต

ควรเข้ารับการรักษาทันที

อย่าปล่อยทิ้งไว้

อาจเสี่ยงต่อการติดเชื้อรุนแรง
"""

        color = "🔴"

    
    # =====================================================
    # RESULT CARD
    # =====================================================

    st.divider()

    st.subheader("📋 ผลการประเมิน")

    with st.container(border=True):

        if predicted_class == "Grade 1":

            st.success(f"{color} {risk_text}")

        elif predicted_class == "Grade 2":

            st.warning(f"{color} {risk_text}")

        elif predicted_class == "Grade 3":

            st.warning(f"{color} {risk_text}")

        else:

            st.error(f"{color} {risk_text}")

        st.metric(
            "ความมั่นใจของ AI",
            f"{confidence:.2f}%"
        )

    # =====================================================
    # RECOMMENDATION
    # =====================================================

    st.divider()

    st.subheader("💡 คำแนะนำการดูแลเบื้องต้น")

    if predicted_class == "Grade 1":

        st.success(recommendation)

    elif predicted_class == "Grade 2":

        st.warning(recommendation)

    elif predicted_class == "Grade 3":

        st.warning(recommendation)

    else:

        st.error(recommendation)

    # =====================================================
    # SAVE TO HISTORY
    # =====================================================

    st.divider()

    if st.button(
        "💾 บันทึกผลการประเมิน",
        use_container_width=True
    ):

        history = pd.read_csv(HISTORY_FILE)

        new_record = pd.DataFrame([{

            "วันที่และเวลา":
                datetime.now().strftime("%d/%m/%Y %H:%M"),

            "ผลการประเมิน":
                risk_text,

            "Confidence":
                round(confidence,2),

            "คำแนะนำ":
                recommendation.replace("\n"," ")

        }])

        history = pd.concat(
            [history,new_record],
            ignore_index=True
        )

        history.to_csv(
            HISTORY_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        st.success("✅ บันทึกผลการประเมินเรียบร้อยแล้ว")

    # =====================================================
    # DISCLAIMER
    # =====================================================

    st.divider()

    st.caption(
        """
⚠️ ระบบ AI นี้ใช้เพื่อคัดกรองเบื้องต้นเท่านั้น

ผลการประเมินไม่สามารถใช้แทนการวินิจฉัยจากแพทย์ได้

หากแผลมีอาการรุนแรง ควรเข้าพบแพทย์ทันที
"""
    )

else:

    st.info(
        "👆 กรุณาอัปโหลดรูปภาพหรือถ่ายภาพแผลเพื่อเริ่มการวิเคราะห์"
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
"""
<div class="footer">

ระบบปัญญาประดิษฐ์สำหรับวิเคราะห์และคัดกรองความเสี่ยงของแผลเบาหวาน

Developed with TensorFlow & Streamlit

</div>
""",
unsafe_allow_html=True)
