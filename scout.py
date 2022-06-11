import streamlit as st
import numpy as np
import pandas as pd
import pickle
from forex_python.converter import CurrencyRates, CurrencyCodes
from PIL import Image



model = pickle.load(open("autoscout.pkl", "rb"))
enc = pickle.load(open("autoscout_encoder.pkl", "rb"))
df = pd.read_csv("final_model.csv")
image = Image.open('autoscout_car.png')

st.set_page_config(page_title='AutoScout Car Price Predictor', page_icon=':car:')
st.image(image)
st.markdown('***')
st.markdown('# <center><span style="color:#286608">AutoScout Car</span> Price Predictor</center>',unsafe_allow_html=True )
st.markdown("#### <center>Use the sidebar to enter your car's specifications.</center>",unsafe_allow_html=True)
st.markdown('***')
user_make_model = st.sidebar.selectbox("Make & Model", df.make_model.unique())
user_body_type = st.sidebar.selectbox("Body Type", df.body_type.unique())
user_gear = st.sidebar.selectbox("Gearing Type", df["Gearing Type"].unique())
user_fuel = st.sidebar.selectbox("Fuel Type", df.Fuel.unique())
user_km = st.sidebar.number_input("KM", 0, 300000,step=10000)
user_age = int(st.sidebar.selectbox("Age", (0,1,2,3)))
user_cc = st.sidebar.number_input("Displacement (cc)", 900,2967,1200,100)
user_hp = st.sidebar.number_input("HP", 55,390,90,10)

car = pd.DataFrame({"make_model" : [user_make_model],
                    "body_type" : [user_body_type],
                    "km" : [user_km],
                    "hp" : [user_hp],
                    "Gearing Type" : [user_gear],
                    "Displacement_cc" : [user_cc],
                    "Fuel": [user_fuel],
                    "Age" : [user_age]})

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """        
st.markdown(hide_table_row_index, unsafe_allow_html=True)            
showdf = car.rename(columns={'make_model': 'Make & Model',
                             'body_type': 'Body Type',
                             'km': 'KM',
                             'hp': 'HP',
                             'Displacement_cc': 'CC'})
st.markdown("#### <center>Your car's specifications.</center>",unsafe_allow_html=True)
st.table(showdf)

cat = car.select_dtypes("object").columns
car[cat] = enc.transform(car[cat])

c = CurrencyRates()
c_codes = CurrencyCodes()
currencies = ['USD']
for i in c.get_rates('USD').keys():
    currencies.append(i)

st.markdown('***')
cur = st.selectbox('Currency that you want to see the value of your vehicle', currencies)
cur_code = c_codes.get_symbol(cur)



c1, c2, c3, c4, c5,c6,c7,c8,c9 = st.columns(9) 
if c5.button('Predict'):
    result = model.predict(car)[0]
    result *= c.get_rate('USD', cur)
    st.success(f"Predicted value of your car :\n {round(result)} {cur_code}")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 