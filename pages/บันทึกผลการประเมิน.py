import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="บันทึกผลการประเมิน",
    page_icon="📋"
)

HISTORY_FILE = "assessment_history.csv"

# =========================
# Theme CSS
# =========================

st.markdown("""
<style>

/* Light Mode */
html:not([data-theme="dark"]) .history-card{
    background:#EEF3FA;      /* Slightly darker than white */
}

/* Dark Mode */
html[data-theme="dark"] .history-card{
    background:#252B36;      /* Slightly lighter than Streamlit dark */
}

.history-card{
    display:flex;
    border-radius:18px;
    overflow:hidden;
    margin-bottom:18px;
    box-shadow:0 2px 8px rgba(0,0,0,.10);
    border:1px solid rgba(120,120,120,.15);
}

.history-title{
    margin:0;
    color:var(--text-color);
    font-size:30px;
    font-weight:700;
}

.history-date{
    margin-top:8px;
    color:var(--text-color);
    opacity:.65;
}

</style>
""", unsafe_allow_html=True)

# =========================

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
            <div class="history-card">

                <div style="
                width:16px;
                min-width:16px;
                background:{color};
                ">
                </div>

                <div style="padding:18px;">

                    <h3 class="history-title">
                        {row['ผลการประเมิน']}
                    </h3>

                    <p class="history-date">
                        บันทึกวันที่ : {row['วันที่และเวลา']}
                    </p>

                </div>

            </div>
            """, unsafe_allow_html=True)
