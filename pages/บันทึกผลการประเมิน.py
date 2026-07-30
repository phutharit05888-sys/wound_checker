import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="บันทึกผลการประเมิน",
    page_icon="📋",
    layout="centered"
)

HISTORY_FILE = "assessment_history.csv"

st.title("📋 บันทึกผลการประเมิน")

if not os.path.exists(HISTORY_FILE):

    st.info("ยังไม่มีข้อมูลการประเมิน")

else:

    history = pd.read_csv(HISTORY_FILE)

    if history.empty:

        st.info("ยังไม่มีข้อมูลการประเมิน")

    else:

        history = history.iloc[::-1]

        for i, row in history.iterrows():

            result = row["ผลการประเมิน"]

            if "เฝ้าระวัง" in result:

                icon = "🟢"

            elif "พบแพทย์" in result and "ด่วน" not in result:

                icon = "🟡"

            else:

                icon = "🔴"

            st.markdown(f"""
            <div style="
            display:flex;
            align-items:center;
            margin-bottom:18px;
            border-radius:22px;
            overflow:hidden;
            background:var(--secondary-background-color);
            border:1px solid rgba(128,128,128,.15);
            ">

            <div style="
            width:14px;
            height:105px;
            background:{color};
            flex-shrink:0;
            ">
            </div>

            <div style="
            padding:20px;
            ">

            <div style="
            font-size:30px;
            font-weight:700;
            color:var(--text-color);
            ">
            {result}
            </div>

            <div style="
            margin-top:8px;
            font-size:16px;
            color:var(--text-color);
            opacity:.65;
            ">
            บันทึกวันที่ : {row['วันที่และเวลา']}
            </div>

            </div>

            </div>
            """, unsafe_allow_html=True)
