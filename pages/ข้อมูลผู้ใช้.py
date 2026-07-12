import streamlit as st
from datetime import date

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
        ["ชาย", "หญิง"]
    )

    dob = st.date_input(
        "วัน/เดือน/ปี เกิด",
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

    st.subheader("🔒 รหัสผ่านสำหรับใช้งานระบบ")

    password = st.text_input(
        "สร้างรหัสผ่าน",
        type="password"
    )

    confirm_password = st.text_input(
        "ยืนยันรหัสผ่าน",
        type="password"
    )

    submitted = st.form_submit_button("ยืนยัน")

if submitted:

    # ตรวจสอบข้อมูล
    if name.strip() == "":
        st.error("กรุณากรอกชื่อ-นามสกุล")

    elif password == "":
        st.error("กรุณาสร้างรหัสผ่าน")

    elif password != confirm_password:
        st.error("รหัสผ่านไม่ตรงกัน")

    else:

        # บันทึกข้อมูลไว้ใน Session
        st.session_state["patient_registered"] = True

        st.session_state["history_password"] = password

        st.session_state["patient"] = {
            "name": name,
            "age": age,
            "gender": gender,
            "dob": str(dob)
        }

        st.success("✅ บันทึกข้อมูลเรียบร้อย!")

        st.info("กรุณาไปที่หน้า AI Detection เพื่อเริ่มตรวจสอบแผล")
