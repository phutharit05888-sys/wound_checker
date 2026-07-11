import streamlit as st

st.title("👤 กรอกข้อมูลผู้ใช้")

with st.form("patient_form"):

    st.subheader("ข้อมูลส่วนตัว")

    name = st.text_input("ชื่อจริง-นามสกุล")

    age = st.number_input(
        "อายุ",
        min_value=1,
        max_value=120
    )

    gender = st.selectbox(
        "เพศ",
        ["ชาย","หญิง"]
    )

    submitted = st.form_submit_button("Continue")

if submitted:

    st.success("Information saved successfully!")

    st.write("Proceed to the AI Detection page.")
