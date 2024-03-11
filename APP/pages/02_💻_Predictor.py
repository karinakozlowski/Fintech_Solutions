import streamlit as st
from service import predict

st.set_page_config(layout="centered")

st.header("Formulario para predecir transacciones fraudulentas")

with st.form("form_predict"):
    st.write("Por favor, ingrese los datos de la transacción")
    step = st.number_input("Dia del mes",min_value=0,max_value=31)
    monto = st.number_input("Monto",min_value=0)
    oldbalanceOrg = st.number_input("Saldo Anterior Origen",min_value=0)
    oldbalanceDest = st.number_input("Saldo Anterior Destino",min_value=0)
    type_transfer = st.selectbox("Tipo de transacción",["Retiro en efectivo","Transferencia"])
    horario = st.selectbox("Horario",["Mañana","Tarde","Noche"])
    fin_de_semana = st.checkbox("¿La transacción se realizó en fin de semana?")
    submitted = st.form_submit_button("Predecir")
    
if submitted: 
    data = {
        "step": step*24,
        "monto": monto,
        "oldbalanceOrg": oldbalanceOrg,
        "oldbalanceDest": oldbalanceDest,
        "type_CASH_OUT": 0,
        "type_TRANSFER": 0,
        "fin_de_semana": fin_de_semana,
        "mañana": 0,
        "noche": 0,
        "tarde": 0
    }
    if type_transfer == "Retiro en efectivo":
        data["type_CASH_OUT"] = 1
    else:
        data["type_TRANSFER"] = 1
    data[f"{horario.lower()}"] = 1
    prediction = predict(data)
    if prediction["prediction"]:
        st.error("Transacción fraudulenta",icon="🚨")
    else:
        st.success("Transacción segura",icon="✅")
    # st.write(data)
    
    
