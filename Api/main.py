from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
import pandas as pd
import time
import joblib

app = FastAPI()

class Transaction(BaseModel):
    monto: float
    mañana: int
    noche: int
    tarde: int
    fin_de_semana: int
    type_TRANSFER: int
    type_CASH_OUT: int

model = None  # Variable global para almacenar el modelo
scaler = None  # Variable global para almacenar el scaler
data = None  # Variable global para almacenar los datos

@app.on_event("startup")
def load_model():
    global model, scaler, data
    # Cargar el modelo
    try:
        model = joblib.load("modelo_gradient_boosting.pkl")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al cargar el modelo. Detalle: {}".format(str(e)))

    # Cargar el scaler
    scaler = StandardScaler()  # O cualquier método para cargar el scaler que hayas utilizado

    # Cargar los datos
    try:
        data = pd.read_parquet("data_tranfo_ml_reducido.parquet")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al cargar los datos. Detalle: {}".format(str(e)))

# Ruta para predecir fraude
@app.post("/predict_fraud/", tags=["Fraud Detection"])
def predict_fraud(transaction: Transaction):
    global model, scaler, data
    if model is None or scaler is None or data is None:
        raise HTTPException(status_code=500, detail="Modelo o datos no cargados. Por favor, espere e intente nuevamente.")
    
    # Esperar hasta que el modelo esté cargado (máximo 10 segundos)
    max_wait_time = 400  # segundos
    wait_interval = 0.5  # segundos
    waited_time = 0

    while model is None and waited_time < max_wait_time:
        time.sleep(wait_interval)
        waited_time += wait_interval

    if model is None:
        raise HTTPException(status_code=500, detail="No se pudo cargar el modelo a tiempo. Intente nuevamente.")

    input_data = [[transaction.monto, transaction.mañana, transaction.noche, transaction.tarde, 
                  transaction.fin_de_semana, 0.0, 0.0,  # Placeholder para oldbalanceDest y oldbalanceOrg
                  transaction.type_TRANSFER, transaction.type_CASH_OUT]]
    
    # Ajustar el StandardScaler si no está ajustado previamente
    if not scaler.mean_:
        scaler.fit(data)  # Ajustar el scaler utilizando los datos de entrenamiento
    
    # Escalar las características
    scaled_data = scaler.transform(input_data)
    
    prediction = model.predict(scaled_data)[0]
    return {"is_fraud": bool(prediction)}