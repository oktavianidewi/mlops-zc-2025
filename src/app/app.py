import streamlit as st

from predict import predict, list_models

st.title("Diabetes Prediction")

st.markdown("Enter client data:")

# Input parameters
pregnancies = st.slider("Pregnancies (months)", 0, 3, 10)
glucose = st.number_input("Glucose", value=70.0)
blood_pressure = st.number_input("Blood Pressure", value=70.0)
skin_thickness = st.number_input("Skin Thickness", value=40.0)
insulin = st.number_input("Insulin", value=90.0)
bmi = st.number_input("BMI", value=40.0)
diabeter_pedigree_function = st.selectbox("Diabetes Pedigree Function", [0, 1])
age = st.slider("Age (years)", 0, 15, 90)

# Input parameters
input_dict = {
    'Pregnancies': pregnancies, 
    'Glucose': glucose, 
    'BloodPressure': blood_pressure, 
    'SkinThickness': skin_thickness, 
    'Insulin': insulin, 
    'BMI': bmi, 
    'DiabetesPedigreeFunction': diabeter_pedigree_function, 
    'Age': age
}

dict_res = {0: 'Not-Diabetes', 1: 'Diabetes'}

# Precidiction
if st.button("Predict"):
    prediction, probability, model_info = predict(input_dict)    
    results = dict_res[prediction]
    st.markdown(f"### Predictions: {results}, {probability}")
    st.markdown(f"Model info: {model_info}")
