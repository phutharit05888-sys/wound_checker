import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="บันทึกผลการประเมิน",
    page_icon="📋"
)

HISTORY_FILE = "assessment_history.csv"

st.title("📋 บันทึกผลการประเมิน")

if os.path.exists(HISTORY_FILE):

    history = pd.read_csv(HISTORY_FILE)

    if len(history)==0:

        st.info("ยังไม่มีข้อมูลการประเมิน")

    else:

        history = history.iloc[::-1]

        for _,row in history.iterrows():

            if row["ผลการประเมิน"]=="ควรดูแลเฝ้าระวัง":

                color="#49C16D"

            elif row["ผลการประเมิน"]=="ควรพบแพทย์":

                color="#FFD54F"

            else:

                color="#F44336"

            st.markdown(f"""
            <div style="
            display:flex;
            background:white;
            border-radius:18px;
            overflow:hidden;
            margin-bottom:18px;
            box-shadow:0px 2px 8px rgba(0,0,0,.1);
            ">

            <div style="
            width:16px;
            background:{color};
            "></div>

            <div style="padding:18px;">

            <h3 style="margin:0;color:#173A75;">
            {row['ผลการประเมิน']}
            </h3>

            <p style="margin-top:8px;color:gray;">
            บันทึกวันที่ : {row['วันที่และเวลา']}
            </p>

            </div>

            </div>
            """,unsafe_allow_html=True)
