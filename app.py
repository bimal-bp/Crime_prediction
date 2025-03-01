import streamlit as st
import pickle
import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import LabelEncoder

# Load the trained model
model = pickle.load(open('Model/model.pkl', 'rb'))

# Define city names and crime types
city_names = [
    'Agra', 'Ahmedabad', 'Bhopal', 'Chennai', 'Delhi', 'Faridabad', 'Ghaziabad',
    'Hyderabad', 'Indore', 'Jaipur', 'Kalyan', 'Kanpur', 'Kolkata', 'Lucknow',
    'Ludhiana', 'Meerut', 'Mumbai', 'Nagpur', 'Nashik', 'Patna', 'Pune', 'Rajkot',
    'Srinagar', 'Surat', 'Thane', 'Varanasi', 'Visakhapatnam'
]

crime_types = [
    'Arson', 'Assault', 'Burglary', 'Counterfeiting', 'Cybercrime', 'Domestic Violence',
    'Drug Offense', 'Extortion', 'Firearm Offense', 'Fraud', 'Homicide', 'Identity Theft',
    'Illegal Possession', 'Kidnapping', 'Public Intoxication', 'Robbery',
    'Sexual Assault', 'Shoplifting', 'Traffic Violation', 'Vandalism', 'Vehicle Stolen'
]

# Population data (in millions)
population_dict = {
    'Agra': 20.50, 'Ahmedabad': 63.50, 'Bhopal': 21.00, 'Chennai': 87.00, 'Delhi': 163.10, 
    'Faridabad': 19.20, 'Ghaziabad': 23.60, 'Hyderabad': 77.50, 'Indore': 21.70, 
    'Jaipur': 30.70, 'Kalyan': 18.40, 'Kanpur': 29.20, 'Kolkata': 141.10, 'Lucknow': 29.00,
    'Ludhiana': 16.80, 'Meerut': 18.90, 'Mumbai': 184.10, 'Nagpur': 25.00, 'Nashik': 22.10,
    'Patna': 20.50, 'Pune': 50.50, 'Rajkot': 14.60, 'Srinagar': 15.30, 'Surat': 45.80,
    'Thane': 17.90, 'Varanasi': 14.00, 'Visakhapatnam': 23.50
}

# Label Encoding for Cities
le = LabelEncoder()
city_encoded = le.fit_transform(city_names)
city_mapping = dict(zip(city_names, city_encoded))

# Streamlit UI
st.title("Crime Rate Prediction App")

# User Inputs
selected_city = st.selectbox("Select City", city_names)
selected_crime = st.selectbox("Select Crime Type", crime_types)
selected_year = st.slider("Select Year", 2020, 2024, 2022)

# Convert user input into model features
city_code = city_mapping[selected_city]
crime_code = crime_types.index(selected_crime)
population = population_dict[selected_city]

# Population adjustment (Assume 1% growth per year)
year_diff = selected_year - 2020
adjusted_population = population + (0.01 * year_diff * population)

# Predict crime rate
if st.button("Predict Crime Rate"):
    crime_rate = model.predict([[selected_year, city_code, adjusted_population, crime_code]])[0]

    # Crime Severity Classification
    if crime_rate <= 1:
        crime_status = "Very Low Crime Area"
    elif crime_rate <= 5:
        crime_status = "Low Crime Area"
    elif crime_rate <= 15:
        crime_status = "High Crime Area"
    else:
        crime_status = "Very High Crime Area"

    # Calculate estimated crime cases
    estimated_cases = math.ceil(crime_rate * adjusted_population)

    # Display results
    st.subheader("Prediction Results")
    st.write(f"**City:** {selected_city}")
    st.write(f"**Crime Type:** {selected_crime}")
    st.write(f"**Year:** {selected_year}")
    st.write(f"**Predicted Crime Status:** {crime_status}")
    st.write(f"**Crime Rate:** {crime_rate:.2f}")
    st.write(f"**Estimated Cases:** {estimated_cases}")
