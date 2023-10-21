import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import folium
import streamlit as st
import numpy as np
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

st.set_page_config(layout="wide")

#######################################################################################
##                                   Sidebar                                         ##
#######################################################################################

image = "images/curry.png"

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

st.header("Marketplace - Visão Restaurantes")

tab1, tab2, tab3 = st.tabs(["Teste", "-", "-"])

with tab1:
  
  with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
      col1.metric('Entregadores únicos', len(df["Delivery_person_ID"].unique()))
      
    with col2:
      cols = ["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"]
      df["Distance"] = df[cols].apply(lambda x: haversine((x["Restaurant_latitude"], x["Restaurant_longitude"]),
                                                          (x["Delivery_location_latitude"], x["Delivery_location_longitude"])), axis=1)
      col2.metric('Distância média (km)', df["Distance"].mean())
      
    with col3:
      col3.metric("Tempo de entrega médio c/ festival", df.loc[df["Festival"] == "Yes", "Time_taken(min)"].mean())
      
    with col4:
      col4.metric("Desvio padrão das entregas médio c/ festival", df.loc[df["Festival"] == "Yes", "Time_taken(min)"].std())
      
    with col5:
      col5.metric("Tempo de Entrega médio sem festival", df.loc[df["Festival"] == "No", "Time_taken(min)"].mean())
      
    with col6:
      col6.metric("Desvio padrão do tempo de entrega sem festival", df.loc[df["Festival"] == "No", "Time_taken(min)"].std())
      
  with st.container():
    st.markdown("##### Distribuição da Distância média por cidade")
    df_aux = df[["City", "Time_taken(min)"]].groupby("City").mean()
    pie_chart = px.pie(df_aux, values="Time_taken(min)", names="Time_taken(min)")
    st.plotly_chart(pie_chart, use_container_width=True)
    
  with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
      st.markdown("##### Distribuição do tempo por cidades")
      df_aux = df[["City", "Time_taken(min)"]].groupby("City").agg({"Time_taken(min)": ["mean", "std"]})
      df_aux.columns = ["time_mean", "time_std"]
      df_aux = df_aux.reset_index()
      
      fig = go.Figure()
      fig.add_trace(go.Bar(name="Control", x=df_aux["City"], y=df_aux["time_mean"], error_y=dict(type="data", array=df_aux["time_std"])))
      fig.update_layout(barmode='group')
      
      st.plotly_chart(fig)
    
    with col2:
      st.markdown("##### Tempo médio por tipo de entrega")
      df_aux = df[["Time_taken(min)", "City", "Type_of_order"]].groupby(["City", "Type_of_order"]).agg({"Time_taken(min)": ["mean", "std"]})
      df_aux.columns = ["time_avg", "time_std"]
      df_aux = df_aux.reset_index()
      st.dataframe(df_aux)

  with st.container():
    st.markdown("##### Tempo médio por cidade")
    df_aux = df[["Time_taken(min)", "City", "Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).agg({"Time_taken(min)": ["mean", "std"]})
    df_aux.columns = ["time_taken_mean", "time_taken_std"]
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=["City", "Road_traffic_density"], values= "time_taken_mean", color="time_taken_std", color_continuous_scale="RdBu",
                     color_continuous_midpoint=np.average(df_aux['time_taken_std']))
    st.plotly_chart(fig)
