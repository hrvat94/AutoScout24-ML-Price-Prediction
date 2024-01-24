import streamlit as st 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import data, api

st.set_page_config(layout="wide")

sns.set_theme(style="whitegrid")

st.header("AutoScout24 - Price Prediction")
st.write("Finde den richtigen Preis für dein Fahrzeug.")

st.sidebar.header("Fahrzeugdetails")


def reset_output():
    st.session_state.clicked = False

make = st.sidebar.selectbox("Marke:",data.df_new['make'].sort_values().unique(), on_change=reset_output)
model = st.sidebar.selectbox("Modell:",data.df_new[(data.df_new['make'] == make)]['model'].sort_values().unique(), on_change=reset_output)
fuel = st.sidebar.selectbox("Kraftstoffart:", data.fuel_dict)
gear = st.sidebar.selectbox("Getriebeart:", data.gear_dict)
offer = st.sidebar.selectbox("Fahrzeugart:", data.offer_dict)
year = st.sidebar.slider("Erstzulassung:",min_value=2011, max_value=2030)
mileage = st.sidebar.slider("Kilometer:",min_value=0, max_value=300000)
hp = st.sidebar.slider("PS:",min_value=0, max_value=850)
kw = round(hp/1.36)
km_dropdown_as24  = [2500, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 125000, 150000, 175000, 200000]

#st.write(km_dropdown_as24)
kmfrom = None
kmto = None
for idx, km in enumerate(km_dropdown_as24):
    if mileage >= 200000:
        kmfrom = 200000
        kmto = None
    elif mileage == 0:
        kmfrom = None
        kmto = 10000
    elif km_dropdown_as24[idx] < mileage <= km_dropdown_as24[idx+1]:
        kmfrom = km_dropdown_as24[idx]
        kmto = km_dropdown_as24[idx+1]
powerfrom = kw-20
powerto = kw+20
if powerfrom < 0:
    powerfrom = 0
fregfrom = year
fregto  = year
 
st.write('Deine Eingabe:')
df_choose = pd.DataFrame(columns=['Marke','Modell', 'Kraftstoffart', 'Getriebeart', 'Fahrzeugart', 'Erstzulassung', 'Kilometer', 'PS', 'kW'])
df_choose.loc[0] = [make, model, fuel, gear, offer, year, mileage, hp, kw]
df_choose.round(2)
st.table(df_choose)

if fuel == 'Benzin':
    fuel_pred = 'Gasoline'
elif fuel == 'Diesel':
    fuel_pred = 'Diesel'
elif fuel == 'Elektro':
    fuel_pred = 'Electric'
elif fuel == 'Hybrid (Elektro/Benzin)':
    fuel_pred = 'Hybrid'
elif fuel == 'Hybrid (Elektro/Diesel)':
    fuel_pred = 'Hybrid'
elif fuel == 'Autogas (LPG)':
    fuel_pred = 'Others'
elif fuel == 'Erdgas (CNG)':
    fuel_pred = 'Others'
elif fuel == 'Ethanol':
    fuel_pred = 'Others'
elif fuel == 'Wasserstoff':
    fuel_pred = 'Others'
elif fuel == 'Sonstige':
    fuel_pred = 'Others'

if gear == 'Automatik':
    gear_pred = 'Automatic'
elif gear == 'Schaltgetriebe':
    gear_pred = 'Manual'
elif gear == 'Halbautomatik':
    gear_pred = 'Semi-automatic'

if offer == 'Gebraucht':
    offer_pred = 'Used'
elif offer == 'Neu':
    offer_pred = 'New'
elif offer == 'Jahreswagen':
    offer_pred = "Employee's car"
elif offer == 'Vorführwagen':
    offer_pred = 'Demonstration'
elif offer == 'Tageszulassung':
    offer_pred = 'Pre-registered'

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

url = api.getURLfromAS24(make, model, data.fuel_dict[fuel], data.gear_dict[gear], year, kmfrom, kmto, powerfrom, powerto, data.offer_dict[offer])
#st.write(url)

if st.session_state.clicked:
    st.write('AutoScout24 Parameter:')
    df_autoscout = pd.DataFrame(columns=['Marke','Modell', 'Kraftstoffart', 'Getriebeart', 'Fahrzeugart', 'Erstzulassung', 'Kilometer von', 'Kilometer bis', 'PS', 'kW von', 'kW bis'])
    df_autoscout.loc[0] = [make, model, data.fuel_dict[fuel], data.gear_dict[gear], data.offer_dict[offer], year, kmfrom, kmto, hp, powerfrom, powerto]
    df_autoscout.round(2)
    st.table(df_autoscout)

    prediction_rf = data.predict_rf(make, model, fuel_pred, gear_pred, offer_pred, mileage, hp, year)
    #st.write(prediction_rf.round(2))

    prediction_lr = data.predict_lr(make, model, fuel_pred, gear_pred, offer_pred, mileage, hp, year)
    #st.write(prediction_lr.round(2))

    st.write('Prediction:')
    df_prediction = pd.DataFrame(columns=['','Random Forest', 'Lineare Regression'])
    df_prediction.loc[0] = ['Preis' ,prediction_rf, prediction_lr]

    df_prediction = df_prediction.style.format(
        {
            "Random Forest": lambda x : '{:,.2f} €'.format(x),
            "Lineare Regression": lambda x : '{:,.2f} €'.format(x)
        },
        thousands='.',
        decimal=',',
    )

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_prediction)

    url_data = api.get_carsData(url)

    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            color: red;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    with col2:
        #st.write(url_data)
        #st.write(url_data[0])

        df_url = pd.DataFrame()

        #st.write(url_data[4])
        #st.write(url_data[4][0])
        try:
            st.image(url_data[4][6])
        except:
            st.markdown('<p class="big-font">No Data for Cars from AutoScout</p>', unsafe_allow_html=True)

    st.write('AutoScout24 Autovergleich:')
    st.write(url)

    #df_url.loc[0] = [url_data[1][0] ,url_data[2][0], url_data[0][0]]
    for i in range(0, len(url_data[1])):
        df_url = pd.concat([df_url, pd.DataFrame([[url_data[1][i] ,url_data[2][i], url_data[6][i],url_data[7][i], url_data[8][i], url_data[9][i], url_data[10][i], url_data[3][i], url_data[0][i]]])], ignore_index=True)

    df_url.rename(columns={0: "Titel", 1: "Beschreibung",2: 'Attribute1', 3: 'Attribute2', 4: 'Attribute3', 5: 'Attribute4', 6: 'Attribute5', 7: 'Link', 8: 'Preis'}, inplace= True)
    df_url = df_url.iloc[1:]
    df_url = df_url.style.format(
        {
            "Preis": lambda x : '{:,.2f}€'.format(x),
        },
        thousands='.',
        decimal=',',
    )

    st.table(df_url)



def clicked():
    st.session_state.clicked = True

st.sidebar.button("Preis anzeigen", on_click= clicked)

