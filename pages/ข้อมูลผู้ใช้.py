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

    from datetime import date

    dob = st.date_input(
        "วัน/เดือน/ปี เกิด",
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    submitted = st.form_submit_button("ยืนยัน")

if submitted:

    st.success("ข้อมูลบันทึกเรียบร้อย!")

    st.write("ไปหน้าตรวจสอบแผล")
