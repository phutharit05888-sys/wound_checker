import streamlit as st

st.title("👤 Patient Information")

with st.form("patient_form"):

    st.subheader("Personal Information")

    name = st.text_input("Patient Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120
    )

    gender = st.selectbox(
        "Gender",
        ["Male","Female"]
    )

    height = st.number_input("Height (cm)")
    weight = st.number_input("Weight (kg)")

    st.subheader("Medical Information")

    diabetes = st.selectbox(
        "Diabetes Type",
        ["Type 1","Type 2","Unknown"]
    )

    duration = st.number_input(
        "Years with Diabetes",
        min_value=0
    )

    wound = st.selectbox(
        "Wound Location",
        [
            "Toe",
            "Heel",
            "Sole",
            "Top of Foot",
            "Side of Foot"
        ]
    )

    submitted = st.form_submit_button("Continue")

if submitted:

    st.success("Information saved successfully!")

    st.write("Proceed to the AI Detection page.")
