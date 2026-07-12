import streamlit as st
import pandas as pd
import os

st.title("📋 ระบบบันทึกผลการประเมิน")

HISTORY_FILE = "assessment_history.csv"

if os.path.exists(HISTORY_FILE):

    df = pd.read_csv(HISTORY_FILE)

    st.dataframe(
        df.drop(columns=["ภาพแผล"]),
        use_container_width=True
    )

else:

    st.info("ยังไม่มีข้อมูลการประเมิน")
