import requests
URL_API = 'https://c16-103-t-data-bi.onrender.com/predict/'


# option with API 
def predict(data):
    response = requests.post(URL_API, json=data)
    prediction = response.json()
    print(prediction)
    return prediction

