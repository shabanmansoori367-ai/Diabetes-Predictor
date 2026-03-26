import streamlit as st
import numpy as np
import joblib
import base64

# 🔹 Load model
model = joblib.load("diabetes_model2.pkl")

# 🔹 Convert image to base64
def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 🔹 Background image (local)
img_base64 = get_base64_image("C:/Users/shaba/Downloads/istockphoto-1189304032-612x612.jpg")

# 🔹 Page config
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="wide"
)

# 🔹 Background + CSS
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.65);
    z-index: 0;
}}

.main-container {{
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 95vh;
}}

.card {{
    background: rgba(255,255,255,0.1);
    padding: 35px;
    border-radius: 25px;
    backdrop-filter: blur(20px);
    width: 750px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
}}

.stButton>button {{
    background: linear-gradient(45deg, #ff512f, #dd2476);
    color: white;
    border-radius: 15px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    border: none;
}}

h1, p, label {{
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# 🔹 Layout
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

# 🔹 Title
st.markdown("<h1>🩺 Diabetes Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p>Enter patient details to check diabetes probability</p>", unsafe_allow_html=True)

# 🔹 Mappings
yes_no_map = {"No": 0, "Yes": 1}

smoking_options = {
    "Never": 0,
    "Former": 1,
    "Current": 2,
    "No Info": 3
}

# 🔹 Inputs
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("👤 Gender", ["Female", "Male"])
    age = st.number_input("🎂 Age", 1, 120, 25)
    selected_hyper = st.selectbox("💓 Hypertension", ["No", "Yes"])
    selected_heart = st.selectbox("❤️ Heart Disease", ["No", "Yes"])

with col2:
    selected_smoking = st.selectbox("🚬 Smoking History", list(smoking_options.keys()))
    bmi = st.number_input("⚖️ BMI", 10.0, 50.0, 25.0)
    hba1c = st.number_input("🧪 HbA1c Level", 3.0, 15.0, 5.5)
    glucose = st.number_input("🩸 Blood Glucose", 50, 300, 100)

# 🔹 Convert inputs
gender = 1.0 if gender == "Male" else 0.0
hypertension = yes_no_map[selected_hyper]
heart_disease = yes_no_map[selected_heart]
smoking_history = smoking_options[selected_smoking]

# 🔹 Prediction
if st.button("🚀 Predict Now"):

    input_data = np.array([[
        gender,
        age,
        hypertension,
        heart_disease,
        smoking_history,
        bmi,
        hba1c,
        glucose
    ]])

    probability = model.predict_proba(input_data)[0][1]

    # 🔹 Risk level
    if probability < 0.3:
        risk = "Low Risk ✅"
        color = "#00ffcc"
    elif probability < 0.7:
        risk = "Medium Risk ⚠️"
        color = "#ffcc00"
    else:
        risk = "High Risk 🚨"
        color = "#ff4d4d"

    # 🔹 Output
    st.markdown(f"""
    <div style="
        text-align:center;
        margin-top:20px;
        padding:20px;
        border-radius:15px;
        background: rgba(0,0,0,0.6);
    ">
        <h2 style="color:{color};">{risk}</h2>
        <h3 style="
            color:{color};
            font-weight:bold;
            text-shadow:0px 0px 10px {color};
        ">
            Probability: {probability*100:.2f}%
        </h3>
    </div>
    """, unsafe_allow_html=True)

# 🔥 🔹 Prevention Tips Button (ENGLISH)
if st.button("💡 Diabetes Prevention Tips"):

    st.markdown("""
    <div style="
        margin-top:20px;
        padding:20px;
        border-radius:15px;
        background: rgba(0,0,0,0.7);
        color:white;
    ">
    <h3>🛡️ Diabetes Prevention Tips:</h3>
    <ul>
        <li>🥗 Eat a healthy diet (low sugar & less junk food)</li>
        <li>🏃 Exercise regularly (at least 30 minutes daily)</li>
        <li>⚖️ Maintain a healthy weight</li>
        <li>🚫 Avoid smoking</li>
        <li>🩸 Monitor blood sugar regularly</li>
        <li>💧 Drink plenty of water</li>
        <li>😴 Get proper sleep (7–8 hours)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# 🔹 Close layout
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)