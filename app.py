import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import base64

# Background image helper
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    body {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .stApp {{
        background-color: rgba(10, 31, 68, 0.7);
        padding: 2rem;
        color: white;
    }}
    h1, label, div, input, select, button {{
        color: white !important;
    }}
    .stButton>button {{
        background-color: #1c3d72;
        color: #ffd700;
        font-weight: bold;
        border-radius: 10px;
    }}
    .stButton>button:hover {{
        background-color: #12305a;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

@st.cache_resource
def load_and_train():
    df = pd.read_csv("Admission_Predict.csv")
    df.columns = df.columns.str.strip()
    df.drop(columns=["Serial_No"], inplace=True)

    X = df.drop(columns="Chance_of_Admit")
    y = df["Chance_of_Admit"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = Sequential([
        Dense(64, activation='relu', input_shape=(7,)),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train_scaled, y_train, epochs=100, verbose=0, validation_split=0.2)

    return model, scaler

def main():
    set_background("background.png")  # Replace with your image file

    st.title("🎓 Graduate Admission Predictor")

    model, scaler = load_and_train()

    st.subheader("Enter your profile details:")

    gre = st.number_input("GRE Score (out of 340)", 0, 340, 310)
    toefl = st.number_input("TOEFL Score (out of 120)", 0, 120, 105)
    university_rating = st.selectbox("University Rating", [1, 2, 3, 4, 5], index=2)
    sop = st.slider("SOP Strength (1-5)", 1.0, 5.0, 3.0, 0.5)
    lor = st.slider("LOR Strength (1-5)", 1.0, 5.0, 3.0, 0.5)
    cgpa = st.number_input("CGPA (out of 10)", 0.0, 10.0, 8.5, 0.1)
    research = st.selectbox("Research Experience", ["No", "Yes"])
    research_val = 1 if research == "Yes" else 0

    input_data = np.array([[gre, toefl, university_rating, sop, lor, cgpa, research_val]])
    input_scaled = scaler.transform(input_data)

    if st.button("Predict Admission Chance"):
        prediction = model.predict(input_scaled)[0][0]
        percent = round(prediction * 100, 2)
        st.markdown(f"### 🎉 Estimated Admission Chance: **{percent}%**")

        if percent > 85:
            st.success("🏅 Tier 1 Universities Recommended:\n- MIT\n- Stanford\n- Harvard\n- UC Berkeley\n- Carnegie Mellon")
        elif percent > 75:
            st.info("🎖 Tier 2 Universities Recommended:\n- Purdue\n- UC Irvine\n- Arizona State\n- NCSU\n- Texas A&M")
        elif percent > 65:
            st.warning("🎗 Tier 3 Universities Recommended:\n- University of Alabama\n- University of Kansas\n- University of Mississippi\n- University of Nebraska\n- University of Tennessee")
        else:
            st.error("🔍 Your profile needs improvement. Consider boosting GRE, CGPA, or SOP for better chances.")

if __name__ == "__main__":
    main()


