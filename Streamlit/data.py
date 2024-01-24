import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
import joblib

sns.set_style("whitegrid")

df = pd.read_csv('autoscout24.csv')

#print(df.shape)
#print(df.head())

df.dropna(inplace = True)
df.drop_duplicates(keep = 'first', inplace = True)
#print(df.shape)
df = df.reset_index(drop=True)
#print(df[(df['hp'] == 1)])
df.at[8652, 'hp'] = 110
#print(df.iloc[8652])
df = df.drop(index=df.iloc[23011].name)

df_new = df[(df.price<=340000)]
df_new = df_new[(df_new.mileage<=300000)]
df_new['fuel'].replace(['Electric/Gasoline', 'Electric/Diesel'],  'Hybrid', inplace=True)
df_new['fuel'].replace(['CNG', 'LPG', 'Others', '-/- (Fuel)', 'Ethanol', 'Hydrogen'], 'Others', inplace=True)
df_new = df_new.reset_index(drop=True)
#print(df_new)

fuel_dict = {'Benzin': 'B',
            'Diesel': 'D',
            'Elektro': 'E',
            'Hybrid (Elektro/Benzin)': '2',
            'Hybrid (Elektro/Diesel)': '3',
            'Autogas (LPG)': 'L',
            'Erdgas (CNG)': 'C',
            'Ethanol': 'M',
            'Wasserstoff': 'H',
            'Sonstige': 'O'
            }

gear_dict = {'Schaltgetriebe': 'M',
            'Automatik': 'A',
            'Halbautomatik': 'S'
            }

offer_dict = {'Gebraucht': 'U', # Used
            'Neu': 'N', # New
            'Jahreswagen': 'J', # Employee's car
             #'Oldtimer':'O', # not in our DataSet
             'Vorführwagen':'D', # Demonstration
             'Tageszulassung':'S' # Pre-registered
            }

#data.predict(make, model, fuel_pred, gear_pred, offer_pred, mileage, hp, year)
def predict_rf(make, model, fuel, gear, offer, mileage, hp, year):
    ohe = joblib.load('ohehotencoder.pkl')
    rf = joblib.load('randomforest.pkl')
    
    param_data = {'mileage': mileage, 'hp': hp, 'year': year}
    df_param = pd.DataFrame(data=param_data , index=[0])
    ohe_data = ohe.transform(np.array([[make, model, fuel, gear, offer]]))

    df_data = pd.concat([df_param, ohe_data], axis = 1)

    prediction = rf.predict(df_data)

    return prediction[0]

def predict_lr(make, model, fuel, gear, offer, mileage, hp, year):
    ohe = joblib.load('ohehotencoder.pkl')
    lr = joblib.load('linearregression.pkl')
    
    param_data = {'mileage': mileage, 'hp': hp, 'year': year}
    df_param = pd.DataFrame(data=param_data , index=[0])
    ohe_data = ohe.transform(np.array([[make, model, fuel, gear, offer]]))

    df_data = pd.concat([df_param, ohe_data], axis = 1)

    prediction = lr.predict(df_data)

    return prediction[0]