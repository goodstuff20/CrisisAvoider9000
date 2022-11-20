import csv
from pandas import *
from itertools import *
from operator import itemgetter
import numpy as np
from sklearn.linear_model import LinearRegression
from statistics import mean
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_url = "/v1"

@app.get(f"{base_url}/city")
def ranking_city(buyout_weight: float,
             housing_lifetime_weight: float,
             environmental_risk_weight: float,
             price_development_weight: float,
             time_slide_value: int,
             ):
    ranking = help(buyout_weight,
             housing_lifetime_weight,
             environmental_risk_weight,
             price_development_weight,
             time_slide_value)
    ranking.sort(key=lambda y: -y[0])
    return ranking[0:20]

@app.get(f"{base_url}/state")
def ranking_state(buyout_weight: float,
             housing_lifetime_weight: float,
             environmental_risk_weight: float,
             price_development_weight: float,
             time_slide_value: int,
             ):
    ranking = help(buyout_weight,
             housing_lifetime_weight,
             environmental_risk_weight,
             price_development_weight,
             time_slide_value)
    ranking.sort(key=lambda y: y[2])
    state_ranking = []
    for k, g in groupby(ranking, itemgetter(2)):
        g = list(g)
        state_entry = []
        state_entry.append(mean([city[0] for city in g]))
        state_entry.append(k)
        for i in range(3, 7):
            state_entry.append(mean([city[i] for city in g]))
        state_ranking.append(tuple(state_entry))
    state_ranking.sort(key=lambda y: -y[0])
    return state_ranking


def help(buyout_weight,
             housing_lifetime_weight,
             environmental_risk_weight,
             price_development_weight,
             time_slide_value):

    file = read_csv('CityData.csv', delimiter=";")

    cities = file['Stadt'].tolist()
    states = file['Bundesland'].tolist()
    buyout = file['Buyout'].tolist()
    housing_lifetime = file['Houselive'].tolist()
    price_development_past_values = zip(file['prev_price1'].tolist(), file['prev_price2'].tolist(), file['prev_price3'].tolist())
    environmental_risk_past_values = zip(file['prev_risk1'].tolist(),file['prev_risk2'].tolist(),file['prev_risk3'].tolist())
    price_development = [predict_linear(list(x), time_slide_value) / x[-1] - 1 for x in price_development_past_values]
    environmental_risk = [min(0.99, predict_linear(list(x), time_slide_value)) for x in environmental_risk_past_values]
    price_development_max = max(price_development)
    price_development_min = min(price_development)
    environmental_risk_max = max(environmental_risk)
    environmental_risk_min = min(environmental_risk)
    buyout_max = max(buyout)
    buyout_min = min(buyout)
    housing_lifetime_max = max(housing_lifetime)
    housing_lifetime_min = min(housing_lifetime)

    buyout_norm = [((x-buyout_min)/(buyout_max-buyout_min)) for x in buyout]
    housing_lifetime_norm = [((x-housing_lifetime_min)/(housing_lifetime_max-housing_lifetime_min)) for x in housing_lifetime]
    price_development_norm = [((x-price_development_min)/(price_development_max-price_development_min-1e-15)) for x in price_development]
    environmental_risk_norm = [((x-environmental_risk_min)/(environmental_risk_max-environmental_risk_min-1e-15)) for x in environmental_risk]

    ranking = zip(buyout_norm, housing_lifetime_norm, price_development_norm, environmental_risk_norm)
    ranking_final = [(a*buyout_weight) + (b*housing_lifetime_weight) + (c*price_development_weight) + (d*environmental_risk_weight) for (a,b,c,d) in ranking]
    ranking = zip(ranking_final, cities, states, buyout, housing_lifetime, environmental_risk, price_development)
    return list(ranking)

def predict_linear(past_values, relative_year_to_predict):
    x = np.arange(len(past_values))[:, None]
    y = np.array(past_values)
    model = LinearRegression().fit(x, y)
    return model.predict([[len(past_values) + relative_year_to_predict - 1]])[0]
