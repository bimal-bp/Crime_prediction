import streamlit as st
import pickle
import math

# Load the trained model
model = pickle.load(open('model (5).pkl', 'rb'))

# City and crime type mappings
city_names = {
    '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', '4': 'Delhi',
    '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', '8': 'Jaipur', '9': 'Kanpur',
    '10': 'Kochi', '11': 'Kolkata', '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai',
    '15': 'Nagpur', '16': 'Patna', '17': 'Pune', '18': 'Surat'
}

crimes_names = {
    '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST',
    '3': 'Crime against Senior Citizen', '4': 'Crime against Children', '5': 'Crime against Women',
    '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9': 'Murder'
}

population = {
    '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60, '6': 77.50,
    '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00,
    '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18': 45.80
}

# Crime prevention suggestions
crime_suggestions = {
    '0': "Encourage educational programs and mentorship initiatives for youth.",
    '1': "Strengthen legal protection and create awareness about rights.",
    '2': "Promote inclusivity and ensure strict legal enforcement.",
    '3': "Enhance neighborhood watch programs and personal security for elders.",
    '4': "Increase child safety measures and strengthen family awareness.",
    '5': "Promote gender equality and enforce strict laws against offenders.",
    '6': "Use strong passwords, be cautious online, and report suspicious activities.",
    '7': "Be vigilant about financial frauds, verify sources before transactions.",
    '8': "Educate children about safety, avoid sharing personal details with strangers.",
    '9': "Improve community policing and strengthen law enforcement presence."
}

# Streamlit App
st.title("🔍 Crime Rate Prediction")

# User inputs
city_code = st.selectbox("📍 Select City", options=list(city_names.keys()), format_func=lambda x: city_names[x])
crime_code = st.selectbox("⚖ Select Crime Type", options=list(crimes_names.keys()), format_func=lambda x: crimes_names[x])
year = st.number_input("📅 Enter Year (2024 and beyond)", min_value=2025, step=1)

if st.button("🚔 Predict Crime Rate"):
    pop = population[city_code]
    year_diff = int(year) - 2017
    pop = pop + 0.01 * year_diff * pop  # Population growth assumption: 1% per year

    # Model prediction
    crime_rate = model.predict([[year, city_code, pop, crime_code]])[0]

    # Determine crime status with color coding
    if crime_rate <= 35:
        crime_status = "🟢 Very Low Crime Area"
        color = "green"
    elif crime_rate <= 135:
        crime_status = "🟡 Low Crime Area"
        color = "yellow"
    elif crime_rate <= 210:
        crime_status = "🟠 High Crime Area"
        color = "orange"
    else:
        crime_status = "🔴 Very High Crime Area"
        color = "red"

    cases = math.ceil(crime_rate * pop)

    # Display results with styling
    st.subheader("🔎 Crime Prediction Results:")
    st.write(f"📍 **City:** {city_names[city_code]}")
    st.write(f"⚖ **Crime Type:** {crimes_names[crime_code]}")
    st.write(f"📅 **Year:** {year}")
    st.markdown(f"<h3 style='color:{color};'>🚔 Predicted Cases: {cases}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{color};'>⚠ Crime Severity: {crime_status}</h3>", unsafe_allow_html=True)

    # Crime Prevention Suggestion
    st.markdown("### 💡 Safety Tip:")
    st.write(f"🛑 {crime_suggestions[crime_code]}")
