import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="บันทึกผลการประเมิน",
    page_icon="📋",
    layout="centered"
)

HISTORY_FILE = "assessment_history.csv"

st.markdown("""
<style>

.card{
    display:flex;
    background:white;
    border-radius:20px;
    overflow:hidden;
    margin-bottom:18px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
}

.bar{
    width:18px;
}

.green{
    background:#49C16D;
}

.yellow{
    background:#FFD23F;
}

.orange{
    background:#FF9800;
}

.red{
    background:#E53935;
}

.content{
    padding:18px;
}

.title{
    font-size:28px;
    font-weight:bold;
    color:#123B78;
}

.date{
    color:#777;
    font-size:16px;
    margin-top:5px;
}

</style>
""", unsafe_allow_html=True)

st.title("📋 บันทึกผลการประเมิน")

if not os.path.exists(HISTORY_FILE):

    st.info("ยังไม่มีข้อมูลการประเมิน")

else:

    df = pd.read_csv(HISTORY_FILE)

    df = df.iloc[::-1]

    for _, row in df.iterrows():

        risk = row["ระดับความเสี่ยง"]

        if risk == "Grade 1":
            color = "green"
            text = "ควรดูแลเฝ้าระวัง"

        elif risk == "Grade 2":
            color = "yellow"
            text = "ควรพบแพทย์"

        elif risk == "Grade 3":
            color = "orange"
            text = "ควรพบแพทย์โดยด่วน"

        else:
            color = "red"
            text = "ควรพบแพทย์โดยด่วน"

        st.markdown(f"""
        <div class="card">

            <div class="bar {color}"></div>

            <div class="content">

                <div class="title">
                    {text}
                </div>

                <div class="date">
                    บันทึกวันที่ : {row['วันที่และเวลาที่ประเมิน']}
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)
