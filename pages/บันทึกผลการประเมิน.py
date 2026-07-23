import streamlit as st
import pandas as pd
import os

HISTORY_FILE = "assessment_history.csv"

st.title("📋 บันทึกผลการประเมิน")

if os.path.exists(HISTORY_FILE):

    df = pd.read_csv(HISTORY_FILE)

    if len(df) == 0:
        st.info("ยังไม่มีข้อมูลการประเมิน")

    else:

        df = df.iloc[::-1]

        for _, row in df.iterrows():

            if row["ผลการประเมิน"] == "ควรดูแลเฝ้าระวัง":
                color = "#46C46A"

            elif row["ผลการประเมิน"] == "ควรพบแพทย์":
                color = "#FFD54F"

            else:
                color = "#F44336"

            st.markdown(f"""
            <div style="
                display:flex;
                background:white;
                border-radius:18px;
                margin-bottom:15px;
                overflow:hidden;
                box-shadow:0 1px 6px rgba(0,0,0,.15);
            ">

                <div style="
                    width:14px;
                    background:{color};
                "></div>

                <div style="padding:18px;">

                    <h3 style="margin:0;color:#163E7A;">
                        {row['ผลการประเมิน']}
                    </h3>

                    <p style="margin-top:6px;color:gray;">
                        บันทึกวันที่ : {row['วันที่และเวลา']}
                    </p>

                </div>

            </div>
            """, unsafe_allow_html=True)

else:
    st.info("ยังไม่มีข้อมูลการประเมิน")
