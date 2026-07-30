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

            with st.container(border=True):

                col1, col2 = st.columns([1, 12])

                with col1:

                    st.markdown(f"# {icon}")

                with col2:

                    st.markdown(f"### {result}")
                    st.caption(f"บันทึกวันที่ : {row['วันที่และเวลา']}")
