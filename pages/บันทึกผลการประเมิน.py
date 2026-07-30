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

    if len(history) == 0:

        st.info("ยังไม่มีข้อมูลการประเมิน")

    else:

        history = history.iloc[::-1]

        for _, row in history.iterrows():

            result = str(row["ผลการประเมิน"])

            # ==========================
            # Choose Color
            # ==========================

            if (
                "Grade 1" in result
                or "เฝ้าระวัง" in result
                or "ควรดูแลเฝ้าระวัง" in result
            ):

                color = "#49C16D"

            elif (
                "Grade 2" in result
                or ("ควรพบแพทย์" in result and "ด่วน" not in result)
            ):

                color = "#FFD54F"

            elif (
                "Grade 3" in result
                or "Grade 4" in result
                or "ด่วน" in result
            ):

                color = "#F44336"

            else:

                color = "#9E9E9E"

            # ==========================
            # Card
            # ==========================

            st.markdown(f"""
            <div style="
            display:flex;
            background:var(--secondary-background-color);
            border-radius:18px;
            overflow:hidden;
            margin-bottom:18px;
            box-shadow:0px 2px 8px rgba(0,0,0,.1);
            ">

            <div style="
            width:16px;
            min-width:16px;
            background:{color};
            "></div>

            <div style="padding:18px;">

            <h3 style="
            margin:0;
            color:var(--text-color);
            ">
            {result}
            </h3>

            <p style="
            margin-top:8px;
            color:var(--text-color);
            opacity:.65;
            ">
            บันทึกวันที่ : {row['วันที่และเวลา']}
            </p>

            </div>

            </div>
            """, unsafe_allow_html=True)
