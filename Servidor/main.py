from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from modelo import predict_fraud
from pydantic import BaseModel


app = FastAPI()
origins = [
    "http://localhost:8080",
    "https://deteccion-fraude.streamlit.app",
    "http://localhost:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionData(BaseModel):
    step: int
    monto: float
    oldbalanceOrg: float
    oldbalanceDest: float
    type_CASH_OUT: int
    type_TRANSFER: int
    fin_de_semana: bool
    mañana: bool
    noche: bool
    tarde: bool

@app.get("/")
async def root():
    return {"message": "Hello World"}

# uvicorn main:app --reload


@app.post("/predict/")
async def predict(data: PredictionData):
    try:
        prediction = predict_fraud(data.dict())
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}