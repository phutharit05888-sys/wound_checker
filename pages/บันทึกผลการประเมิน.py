import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="บันทึกผลการประเมิน",
    page_icon="📋",
    layout="centered"
)

HISTORY_FILE = "assessment_history.csv"

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

/* Push page down slightly */
.block-container{
    padding-top:5rem;
}

/* ---------- Light Mode ---------- */

html:not([data-theme="dark"]) .history-card{
    background:#F7FAFF;
    border:1px solid #D8E3F2;
}

/* ---------- Dark Mode ---------- */

html[data-theme="dark"] .history-card{
    background:#232730;
    border:1px solid #3C4350;
}

/* Card */

.history-card{

    display:flex;

    border-radius:20px;

    overflow:hidden;

    margin-bottom:18px;

    box-shadow:0px 2px 10px rgba(0,0,0,.10);

}

/* Left color bar */

.history-bar{

    width:16px;

}

/* Text */

.history-title{

    font-size:30px;

    font-weight:700;

    color:var(--text-color);

    margin:0;

}

.history-date{

    color:var(--text-color);

    opacity:.65;

    margin-top:10px;

    font-size:16px;

}

</style>
""", unsafe_allow_html=True)

# ======================================================
# TITLE
# ======================================================

st.title("📋 บันทึกผลการประเมิน")

# ======================================================
# READ HISTORY
# ======================================================

if not os.path.exists(HISTORY_FILE):

    st.info("ยังไม่มีข้อมูลการประเมิน")

else:

    history = pd.read_csv(HISTORY_FILE)

    if history.empty:

        st.info("ยังไม่มีข้อมูลการประเมิน")

    else:

        # Show newest first
        history = history.iloc[::-1]

        for _, row in history.iterrows():

            result = str(row["ผลการประเมิน"])

            # -------------------------
            # Choose color
            # -------------------------

            if "เฝ้าระวัง" in result or "Grade 1" in result:

                color = "#43C463"

            elif "พบแพทย์" in result or "Grade 2" in result:

                color = "#FFD54F"

            else:

                color = "#F44336"

            # -------------------------
            # Card
            # -------------------------

            st.markdown(f"""
            <div class="history-card">

                <div class="history-bar"
                style="background:{color};">
                </div>

                <div style="padding:22px;">

                    <div class="history-title">

                        {result}

                    </div>

                    <div class="history-date">

                        บันทึกวันที่ :
                        {row["วันที่และเวลา"]}

                    </div>

                </div>

            </div>
            """, unsafe_allow_html=True)
