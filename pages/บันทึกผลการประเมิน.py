import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Assessment History",
    page_icon="📋"
)


st.title(
    "📋 ระบบบันทึกผลการประเมิน (Assessment History)"
)


PASSWORD = "1234"


history_file = "assessment_history.csv"


if not os.path.exists(history_file):

    st.info(
        "ยังไม่มีประวัติการประเมิน"
    )

    st.stop()


data = pd.read_csv(
    history_file
)


st.subheader(
    "รายการประเมินทั้งหมด"
)


st.dataframe(
    data.drop(columns=["ภาพแผล"]),
    use_container_width=True
)


st.divider()


st.subheader(
    "🔒 ดูภาพแผลที่ใช้ในการประเมิน"
)


password = st.text_input(
    "กรอกรหัสผ่านเพื่อดูภาพ",
    type="password"
)


if password == PASSWORD:

    st.success(
        "เข้าถึงภาพสำเร็จ"
    )


    selected = st.selectbox(
        "เลือกวันที่ประเมิน",
        data["วันที่และเวลา"]
    )


    row = data[
        data["วันที่และเวลา"] == selected
    ].iloc[0]


    image_path = row["ภาพแผล"]


    if os.path.exists(image_path):

        st.image(
            image_path,
            caption="ภาพแผลที่ใช้ประเมิน",
            use_container_width=True
        )


        st.write(
            "ระดับความเสี่ยง:",
            row["ระดับความเสี่ยง"]
        )


        st.write(
            "คำแนะนำ:",
            row["คำแนะนำเบื้องต้น"]
        )


else:

    if password != "":
        st.error(
            "รหัสผ่านไม่ถูกต้อง"
        )
