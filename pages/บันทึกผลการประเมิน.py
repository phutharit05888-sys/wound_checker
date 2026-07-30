result = str(row["ผลการประเมิน"])

# ----------------------------------
# Choose stripe color
# ----------------------------------

if "เฝ้าระวัง" in result or "Grade 1" in result:
    color = "#43C463"

elif "พบแพทย์" in result and "ด่วน" not in result:
    color = "#FFD54F"

else:
    color = "#F44336"

# ----------------------------------
# Card
# ----------------------------------

with st.container():

    left, right = st.columns([0.12, 8], gap="small")

    with left:
        st.markdown(
            f"""
            <div style="
                background:{color};
                width:14px;
                height:95px;
                border-radius:12px;
                margin:auto;
            "></div>
            """,
            unsafe_allow_html=True,
        )

    with right:

        with st.container(border=True):

            st.markdown(
                f"""
                <div style="font-size:28px;font-weight:700;">
                {result}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(
                f"บันทึกวันที่ : {row['วันที่และเวลา']}"
            )
