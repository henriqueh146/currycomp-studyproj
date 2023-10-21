import pandas as pd
import plotly.express as px
import pandas as pd
import folium
import streamlit as st
import datetime

from haversine import haversine
from streamlit_folium import folium_static


df_raw = pd.read_csv('dataset/train.csv')

df = df_raw.copy()

# Removing NaNs
df = df.loc[df["Delivery_person_Age"] != "NaN ", :]
df = df.loc[df["Weatherconditions"] != "conditions NaN", :]
df = df.loc[df["Road_traffic_density"] != "NaN ", :]
df = df.loc[df["multiple_deliveries"] != "NaN ", :]
df = df.loc[df["Festival"] != "NaN ", :]
df = df.loc[df["City"] != "NaN ", :]

# Removing extra spaces
df["Road_traffic_density"] = df["Road_traffic_density"].str.strip()
df["Type_of_order"] = df["Type_of_order"].str.strip()
df["Type_of_vehicle"] = df["Type_of_vehicle"].str.strip()
df["Festival"] = df["Festival"].str.strip()
df["City"] = df["City"].str.strip()

# Removing (min) string from Time_taken(min) column
df["Time_taken(min)"] = df["Time_taken(min)"].apply(lambda x: x.split(' ')[1])

# Converting numerical data as object to numerical types
df["Delivery_person_Age"] = df["Delivery_person_Age"].astype(int)
df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].astype(float)
df["multiple_deliveries"] = df["multiple_deliveries"].astype(int)
df["Time_taken(min)"] = df["Time_taken(min)"].astype(int)

# Converting date string to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y")

# Adding week_of_year column
df['week_of_year'] = df['Order_Date'].dt.strftime( "%U" )

#######################################################################################
##                                   Sidebar                                         ##
#######################################################################################

image = "images/curry.png"

st.set_page_config(layout='wide')

st.sidebar.image(image, width=120)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")

date_slider = st.sidebar.slider(
  'Até qual valor?',
  value = datetime.datetime(2022, 4, 13),
  min_value = datetime.datetime(2022, 2, 11),
  max_value = datetime.datetime(2022, 4, 6),
  format = 'DD-MM-YYYY')

st.sidebar.markdown("""---""")

# st.header(date_slider)

traffic_selector = st.sidebar.multiselect(
  'Quais as condições de trânsito',
  ['High', 'Jam', 'Low', 'Medium'],
  ['High', 'Jam', 'Low', 'Medium'])
# st.header(traffic_selector)

st.sidebar.markdown("""---""")
st.sidebar.markdown("## Powered by Comunidade DS")

df = df.loc[df["Order_Date"] <= date_slider, :]
df = df.loc[df["Road_traffic_density"].isin(traffic_selector), :]
#######################################################################################
##                                   Layout                                          ##
#######################################################################################

st.header("Marketplace - Visão Entregadores")

tab1, tab2, tab3 = st.tabs(['Estratégica', '-', '-'])

with tab1:
  with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
      col1.metric("Maior idade", df["Delivery_person_Age"].max())
      
    with col2:
      col2.metric("Menor idade", df["Delivery_person_Age"].min())
      
    with col3:
      col3.metric("Melhor condição de veículos", df["Vehicle_condition"].max())
      
    with col4:
      col4.metric("Pior condição de veículos", df["Vehicle_condition"].min())

    
  with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
      st.markdown("##### Avaliações médias por entregador")
      st.dataframe(df[["Delivery_person_ID", "Delivery_person_Ratings"]].groupby("Delivery_person_ID").mean().reset_index(), use_container_width=True)
      
    with col2:
      
      with st.container():
        st.markdown("##### Avaliações médias por trânsito")
        mean_std_ratings = df[["Delivery_person_Ratings", "Road_traffic_density"]].groupby("Road_traffic_density").agg({"Delivery_person_Ratings": ["mean", "std"]})
        mean_std_ratings.columns = ["ratings_mean", "ratings_std"]
        st.dataframe(mean_std_ratings.reset_index())
        
      with st.container():
        st.markdown("##### Avaliações médias por condições climáticas")
        ratings_per_weather = df[["Delivery_person_Ratings", "Weatherconditions"]].groupby("Weatherconditions").agg({"Delivery_person_Ratings": ["mean", "std"]})
        ratings_per_weather.columns = ["ratings_mean", "ratings_std"]
        st.dataframe(ratings_per_weather.reset_index())
  
  with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
      st.markdown("##### Top entregadores mais rápidos")
      all_cities = df[["City", "Delivery_person_ID", "Time_taken(min)"]].groupby(["City", "Delivery_person_ID"]).mean().reset_index()
      metropolitian = all_cities.loc[all_cities["City"] == "Metropolitian"].sort_values("Time_taken(min)", ascending=True).head(10)
      semi_urban = all_cities.loc[all_cities["City"] == "Semi-Urban"].sort_values("Time_taken(min)", ascending=True).head(10)
      urban = all_cities.loc[all_cities["City"] == "Urban"].sort_values("Time_taken(min)", ascending=True).head(10)
      df_result = pd.concat([metropolitian, semi_urban, urban]).reset_index(drop=True)
      st.dataframe(df_result)
      
    with col2:
      st.markdown("##### Top entregadores mais lentos")
      all_cities = df[["City", "Delivery_person_ID", "Time_taken(min)"]].groupby(["City", "Delivery_person_ID"]).mean().reset_index()
      metropolitian = all_cities.loc[all_cities["City"] == "Metropolitian"].sort_values("Time_taken(min)", ascending=False).head(10)
      semi_urban = all_cities.loc[all_cities["City"] == "Semi-Urban"].sort_values("Time_taken(min)", ascending=False).head(10)
      urban = all_cities.loc[all_cities["City"] == "Urban"].sort_values("Time_taken(min)", ascending=False).head(10)
      df_result = pd.concat([metropolitian, semi_urban, urban]).reset_index(drop=True)
      st.dataframe(df_result)
