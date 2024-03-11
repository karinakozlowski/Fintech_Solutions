import json
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
modelo = joblib.load('modelo.pkl')
scaler = joblib.load('scaler.pkl')
def predict_fraud(data):  
    data = pd.DataFrame([data])
    print(data.info())
    print(data)
    data = data.values.reshape(1, -1)
    data = scaler.transform(data)
    print("transform",data)
    prediction = modelo.predict(data)
    print("prediction",prediction[0])
    isFraud = True if prediction[0] == 1 else False
    return isFraud
    