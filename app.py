import streamlit as st
import numpy as np
import base64

# ----- Background Image Setup -----
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    body {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    .stApp {{
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 2rem;
    }}
    h1, label, input, select, .stSlider, .stButton, .stNumberInput > div > div > input {{
        color: white !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("background.png")

# ----- App Title -----
st.markdown("<h1 style='text-align: center; color: #ff3c3c;'>GRE Admission Predictor</h1>", unsafe_allow_html=True)

# ----- User Input Form -----
gre = st.number_input("GRE Score (out of 340)", min_value=260, max_value=340)
toefl = st.number_input("TOEFL Score (out of 120)", min_value=0, max_value=120)
university_rating = st.selectbox("University Rating", [1, 2, 3, 4, 5])
sop = st.slider("Statement of Purpose (SOP) Strength", 1.0, 5.0, 3.0)
lor = st.slider("Letter of Recommendation (LOR) Strength", 1.0, 5.0, 3.0)
cgpa = st.number_input("CGPA (out of 10)", min_value=0.0, max_value=10.0)
research = st.checkbox("Have Research Experience?")

# ----- Predict Button -----
if st.button("Predict Admission Chance"):
    # Fake result logic (can be replaced later)
    st.success("Estimated Chance of Admission: 78.32%")


