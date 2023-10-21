import pandas as pd
import plotly.express as px
import folium
import streamlit as st

from haversine import haversine
from streamlit_folium import folium_static

from utils.utils import CleanCurryCompData

df_raw = pd.read_csv('dataset/train.csv')

df = df_raw.copy()

df = CleanCurryCompData.clean_data(df)

# # Removing NaNs
# df = df.loc[df["Delivery_person_Age"] != "NaN ", :]
# df = df.loc[df["Weatherconditions"] != "conditions NaN", :]
# df = df.loc[df["Road_traffic_density"] != "NaN ", :]
# df = df.loc[df["multiple_deliveries"] != "NaN ", :]
# df = df.loc[df["Festival"] != "NaN ", :]
# df = df.loc[df["City"] != "NaN ", :]

# # Removing extra spaces
# df["Road_traffic_density"] = df["Road_traffic_density"].str.strip()
# df["Type_of_order"] = df["Type_of_order"].str.strip()
# df["Type_of_vehicle"] = df["Type_of_vehicle"].str.strip()
# df["Festival"] = df["Festival"].str.strip()
# df["City"] = df["City"].str.strip()

# # Removing (min) string from Time_taken(min) column
# df["Time_taken(min)"] = df["Time_taken(min)"].apply(lambda x: x.split(' ')[1])

# # Converting numerical data as object to numerical types
# df["Delivery_person_Age"] = df["Delivery_person_Age"].astype(int)
# df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].astype(float)
# df["multiple_deliveries"] = df["multiple_deliveries"].astype(int)
# df["Time_taken(min)"] = df["Time_taken(min)"].astype(int)

# # Converting date string to datetime
# df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y")

# # Adding week_of_year column
# df['week_of_year'] = df['Order_Date'].dt.strftime( "%U" )

st.set_page_config(layout="wide")

st.title("Visão Empresa")

st.header("Marketplace - Visão Cliente")

#######################################################################################
##                                   Sidebar                                         ##
#######################################################################################

image = "images/curry.png"
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown("## Fastest Delivery in Town")
st.sidebar.markdown("""---""")

# date_slider = st.sidebar.slider(
#   'Até qual valor?',
#   value = pd.datetime(2022, 4, 13),
#   min_value = pd.datetime(2022, 2, 11),
#   max_value = pd.datetime(2022, 4, 6),
#   format = 'DD-MM-YYYY')
import datetime
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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográrica'])

with tab1:
  orders_by_date = df.loc[df["Order_Date"] <= date_slider, ["ID", "Order_Date"]].groupby(["Order_Date"]).count().reset_index()
  orders_by_date.columns = ["Order Date", "Amount"]
  st.header('Orders by Day')
  bar_chart = px.bar(orders_by_date, x='Order Date', y='Amount')# , legendgrouptitle=dict(font=dict(color="black")))
  bar_chart.update_traces(legendgrouptitle=dict(font=dict(color="white")))
  
  st.plotly_chart(bar_chart, use_container_width=True)
  
  col1, col2 = st.columns(2)
  
  with col1:
    # df["Road_traffic_density"] == traffic_selector
    st.header("Traffic Order Share")
    orders_by_traffic = df.loc[:, ["Road_traffic_density", "ID"]].groupby(["Road_traffic_density"]).count().reset_index()
    total = orders_by_traffic["ID"].sum()
    orders_by_traffic["percent"] = orders_by_traffic["ID"] / total
    pie_chart = px.pie(orders_by_traffic, values="percent", names="Road_traffic_density")
    st.plotly_chart(pie_chart, use_container_width=True)
    
  with col2:
    st.header("Traffic Order City")
    volume_per_city = df.loc[:, ["City", "Road_traffic_density", "ID"]].groupby(["City", "Road_traffic_density"]).count().reset_index()
    sc_chart = px.scatter(volume_per_city, x="City", y="Road_traffic_density", size="ID", color="City")
    st.plotly_chart(sc_chart, use_container_width=True)

with tab2:
  st.header("Strategic")
  
  st.markdown("# Deliveries by Week")
  orders_by_week = df.loc[:, ["week_of_year", "ID"]].groupby(["week_of_year"]).count().reset_index().sort_values("week_of_year", ascending=True)
  orders_by_week.columns = ["Week", "Amount"]
  delivery_by_week = px.line(orders_by_week, x="Week", y="Amount", title="Orders By Week")
  st.plotly_chart(delivery_by_week, use_container_width=True)

  st.markdown("# Delivery Share by Week")
  deliveries_by_week = df.loc[:, ["week_of_year", "ID"]].groupby(["week_of_year"]).count().reset_index()
  persons_by_week = df.loc[:, ["week_of_year", "Delivery_person_ID"]].groupby(["week_of_year"]).nunique().reset_index()
  deliveries_per_person_per_week = deliveries_by_week.merge(persons_by_week)
  deliveries_per_person_per_week["deliveries_person_ratio"] = deliveries_per_person_per_week["ID"] / deliveries_per_person_per_week["Delivery_person_ID"]
  delivery_share_graph = px.line(deliveries_per_person_per_week, x="week_of_year", y="deliveries_person_ratio")
  st.plotly_chart(delivery_share_graph, use_container_width=True)

with tab3:
  st.header("Maps")
  
  data_map = df.loc[:, ["City", "Road_traffic_density", "Delivery_location_latitude", "Delivery_location_longitude"]].groupby(["City", "Road_traffic_density"]).median().reset_index()
  map = folium.Map()
  for index, location_info in data_map.iterrows():
    folium.Marker(location=[location_info["Delivery_location_latitude"], location_info["Delivery_location_longitude"]], popup=location_info[["City", "Road_traffic_density"]]).add_to(map)
  
  folium_static(map, width=1024, height=600)