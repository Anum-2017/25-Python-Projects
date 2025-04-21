import streamlit as st
import pandas as pd

st.set_page_config(page_title='BMI Calculator', page_icon='⚖️', layout='wide')

def calculate_bmi(height, weight):
    return weight / ((height / 100) ** 2)

# Custom CSS for better styling
st.markdown("""
    <style>
        .stApp {background-color: #121212; color: white; text-align: center;}
        .stSlider label, .stMarkdown, .stSubheader {color: white !important;}
        .stProgress > div > div > div { border-radius: 10px; }
        .metric-container {text-align: center; font-size: 24px; font-weight: bold; padding: 10px; border-radius: 10px;}
        .footer {text-align: center; font-size: 16px; margin-top: 20px; color: #bbb;}
        .tip-container {text-align: center; font-size: 18px; font-weight: bold; margin-top: 20px; color: #f1c40f;}
        .title-container {text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; color: #e67e22;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title-container'>⚖️ BMI Calculator</div>", unsafe_allow_html=True)

st.markdown("**BMI (Body Mass Index):** BMI helps assess body fat and overall health risks based on weight and height.", unsafe_allow_html=True)

st.markdown("### 🔍 Enter Your Details", unsafe_allow_html=True)

# Input section with improved layout
col1, col2 = st.columns([1, 1])
with col1:
    height = st.slider('📏 **Height (cm)**', 100, 250, 170)
with col2:
    weight = st.slider('⚖️ **Weight (kg)**', 30, 200, 70)

bmi = calculate_bmi(height, weight)

st.markdown("---")
st.subheader("📊 Your BMI Result")

# BMI Category and Styling
if bmi < 18.5:
    category = "Underweight"
    color = "#3498db"  # Blue
    emoji = "😟"
elif 18.5 <= bmi < 25:
    category = "Normal weight"
    color = "#2ecc71"  # Green
    emoji = "😊"
elif 25 <= bmi < 30:
    category = "Overweight"
    color = "#f39c12"  # Orange
    emoji = "😬"
else:
    category = "Obesity"
    color = "#e74c3c"  # Red
    emoji = "😲"

# Display BMI result with better styling
st.markdown(f'<div class="metric-container" style="background-color:{color}; color:white;">Your BMI: {bmi:.2f} {emoji}</div>', unsafe_allow_html=True)
st.progress(min(bmi / 40, 1.0))

st.markdown(f'<p style="color:{color}; font-size:22px; font-weight:bold;">Category: {category}</p>', unsafe_allow_html=True)

st.markdown("### 📌 BMI Categories", unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.info("🔵 Underweight: BMI < 18.5")
    st.success("🟢 Normal weight: 18.5 - 24.9")
with col4:
    st.warning("🟠 Overweight: 25 - 29.9")
    st.error("🔴 Obesity: BMI ≥ 30")

st.markdown("---")
st.markdown("<div class='tip-container'>💡 Tip: Maintain a balanced diet and regular exercise for a healthy BMI!</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Developed by <b>Anum Kamal</b> 💜 | Powered by Streamlit</div>", unsafe_allow_html=True)

