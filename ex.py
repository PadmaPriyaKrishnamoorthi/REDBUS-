import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Database Connection
DB_CONNECTION_STRING = "mysql+pymysql://root:1111@localhost:3306/redbus"
engine = create_engine(DB_CONNECTION_STRING)

# Function to Fetch Unique States
def fetch_states():
    query = "SELECT DISTINCT State_Name FROM bus_details"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        states = [row[0].strip() for row in result.fetchall()]
    return states

# Function to Fetch Unique Routes Based on State
def fetch_routes(state_name):
    query = "SELECT DISTINCT Route_Name FROM bus_details WHERE State_Name = :state_name"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"state_name": state_name})
        routes = [row[0].strip() for row in result.fetchall()]
    return routes

# Function to Fetch Unique Sources Based on State
def fetch_sources(state_name):
    query = "SELECT DISTINCT Source FROM bus_details WHERE State_Name = :state_name"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"state_name": state_name})
        sources = [row[0].strip() for row in result.fetchall()]
    return sources

# Function to Fetch Unique Destinations Based on State
def fetch_destinations(state_name):
    query = "SELECT DISTINCT Destination FROM bus_details WHERE State_Name = :state_name"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"state_name": state_name})
        destinations = [row[0].strip() for row in result.fetchall()]
    return destinations

# Function to Fetch Filtered Data
def fetch_filtered_data(route_name=None, source=None, destination=None, min_price=None, max_price=None, star_rating=None):
    query = "SELECT * FROM bus_details WHERE 1=1"
    params = {}

    if route_name:
        query += " AND Route_Name = :route_name"
        params["route_name"] = route_name

    if source:
        query += " AND Source = :source"
        params["source"] = source

    if destination:
        query += " AND Destination = :destination"
        params["destination"] = destination

    if min_price is not None:
        query += " AND Price >= :min_price"
        params["min_price"] = min_price

    if max_price is not None:
        query += " AND Price <= :max_price"
        params["max_price"] = max_price

    if star_rating:
        query += " AND Star_Rating = :star_rating"
        params["star_rating"] = star_rating

    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        data = result.fetchall()

    columns = result.keys()
    df = pd.DataFrame(data, columns=columns)
    return df

# Sidebar Filters
def display_sidebar_filters():
    states = fetch_states()
    selected_state = st.sidebar.selectbox('Select State', [None] + states)

    selected_route, selected_source, selected_destination = None, None, None

    if selected_state:
        route_names = fetch_routes(selected_state)
        selected_route = st.sidebar.selectbox('Select Route Name', [None] + route_names)

        sources = fetch_sources(selected_state)
        selected_source = st.sidebar.selectbox('Select Source', [None] + sources)

        destinations = fetch_destinations(selected_state)
        selected_destination = st.sidebar.selectbox('Select Destination', [None] + destinations)

    min_price = st.sidebar.number_input('Min Price', min_value=0, value=0)
    max_price = st.sidebar.number_input('Max Price', min_value=0, value=10000)
    star_rating = st.sidebar.selectbox('Star Rating', [None, 3, 4, 5])

    filters = {
        "state_name": selected_state,
        "route_name": selected_route,
        "source": selected_source,
        "destination": selected_destination,
        "min_price": min_price,
        "max_price": max_price,
        "star_rating": star_rating
    }

    return filters

# Main Function
def main():
    st.set_page_config(page_title="Red Bus Data", page_icon="🚌", layout="wide")
    st.title('🚌 Red Bus Data Scraping with Selenium & Dynamic Filtering using Streamlit')

    filters = display_sidebar_filters()

    if st.sidebar.button("Go"):
        filtered_data = fetch_filtered_data(
            route_name=filters["route_name"],
            source=filters["source"],
            destination=filters["destination"],
            min_price=filters["min_price"],
            max_price=filters["max_price"],
            star_rating=filters["star_rating"]
        )
        if not filtered_data.empty:
            st.write(f"### Filtered Data for Route: {filters['route_name']}")
            st.dataframe(filtered_data)
        else:
            st.warning("No data found for the selected filters.")
            st.image(r"C:\Users\Vishwa\Desktop\GUVI captone\RS\planredbus.webp", width=450)

if __name__ == "__main__":
    main()
