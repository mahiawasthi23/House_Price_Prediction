import streamlit as st
import pandas as pd
import joblib
from datetime import datetime


model = joblib.load("house_price_model.pkl")

st.set_page_config(page_title="🏠 House Price Prediction", layout="centered")

st.title("🏠 House Price Prediction")
st.write("Fill the details below to predict house price")

current_year = datetime.now().year


with st.form("house_form"):
    area = st.number_input("Area (sq ft)", min_value=500, max_value=10000, step=100)
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, step=1)
    bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, step=1)
    floors = st.number_input("Floors", min_value=1, max_value=5, step=1)
    year_built = st.number_input("Year Built", min_value=1900, max_value=current_year, step=1)
    garage = st.selectbox("Garage", ["No", "Yes"])
    location = st.selectbox("Location", ["Rural", "Suburban", "Urban"])
    condition = st.selectbox("Condition", ["Fair", "Good", "Poor"])
    
    submitted = st.form_submit_button("Predict Price")


errors = []

if bedrooms > floors * 3:  
    errors.append("Bedrooms seem too high compared to number of floors.")

if bathrooms > bedrooms * 2:
    errors.append("Bathrooms count unusually high for the number of bedrooms.")

if year_built > current_year:
    errors.append("Year Built cannot be in the future.")

if area < bedrooms * 200:
    errors.append("Area seems too small for the number of bedrooms.")

if errors:
    for err in errors:
        st.error(err)
    can_predict = False
else:
    can_predict = True


if submitted:
    if can_predict:
        garage_num = 1 if garage == "Yes" else 0
        data = {
            "Area": area,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
            "Floors": floors,
            "YearBuilt": year_built,
            "Garage": garage_num,
            "Location_Rural": 1 if location == "Rural" else 0,
            "Location_Suburban": 1 if location == "Suburban" else 0,
            "Location_Urban": 1 if location == "Urban" else 0,
            "Condition_Fair": 1 if condition == "Fair" else 0,
            "Condition_Good": 1 if condition == "Good" else 0,
            "Condition_Poor": 1 if condition == "Poor" else 0,
        }
        input_df = pd.DataFrame([data])

        with st.spinner("Predicting house price..."):
            prediction = model.predict(input_df)[0]
        st.success(f"💰 Estimated House Price: ₹ {int(prediction):,}")
    else:
        st.warning("Please fix the errors above before predicting.")
