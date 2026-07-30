import streamlit as st
import pandas as pd
import os

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="บันทึกผลการประเมิน",
    page_icon="📋",
    layout="centered"
)

HISTORY_FILE = "assessment_history.csv"

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

/* Push page down */

.block-container{
    padding-top:5rem;
}

/* Remove default top padding */

main{
    padding-top:0rem;
}

/* ---------- HISTORY CARD ---------- */

.history-card{

    display:flex;

    align-items:center;

    margin-bottom:20px;

    border-radius:22px;

    overflow:hidden;

    transition:.2s;

    border:1px solid rgba(120,120,120,.15);

    box-shadow:0 2px 8px rgba(0,0,0,.08);

}

/* Hover */

.history-card:hover{

    transform:translateY(-2px);

}

/* ---------- LIGHT MODE ---------- */

html:not([data-theme="dark"]) .history-card{

    background:#EDF3FA;

}

/* ---------- DARK MODE ---------- */

html[data-theme="dark"] .history-card{

    background:#262B36;

}

/* ---------- COLOR BAR ---------- */

.history-bar{

    width:16px;

    min-width:16px;

    align-self:stretch;

}

/* ---------- CONTENT ---------- */

.history-content{

    padding:22px;

}

/* ---------- TITLE ---------- */

.history-title{

    font-size:30px;

    font-weight:700;

    color:var(--text-color);

    margin:0;

}

/* ---------- DATE ---------- */

.history-date{

    color:var(--text-color);

    opacity:.65;

    font-size:16px;

    margin-top:8px;

}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.title("📋 บันทึกผลการประเมิน")

# ==========================================
# LOAD HISTORY
# ==========================================

if not os.path.exists(HISTORY_FILE):

    st.info("ยังไม่มีข้อมูลการประเมิน")

else:

    history = pd.read_csv(HISTORY_FILE)

    if history.empty:

        st.info("ยังไม่มีข้อมูลการประเมิน")

    else:

        # newest first
        history = history.iloc[::-1]

        for _, row in history.iterrows():

            result = str(row["ผลการประเมิน"])

            # ---------- Stripe Color ----------

            if "เฝ้าระวัง" in result or "Grade 1" in result:

                color = "#42C96D"

            elif "พบแพทย์" in result and "ด่วน" not in result:

                color = "#FFD54F"

            else:

                color = "#F44336"
# ==========================================
# HISTORY CARD
# ==========================================

st.markdown(f"""
<div class="history-card">

    <div class="history-bar"
         style="background:{color};">
    </div>

    <div class="history-content">

        <div class="history-title">
            {result}
        </div>

        <div class="history-date">
            บันทึกวันที่ : {row["วันที่และเวลา"]}
        </div>

    </div>

</div>
""", unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

st.caption(
    "ระบบบันทึกผลการประเมินด้วย AI สำหรับการคัดกรองความเสี่ยงของแผลเบาหวาน"
)
