import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Database Connection (Update with your database credentials)
DB_CONNECTION_STRING = "mysql+pymysql://root:1111@localhost:3306/redbus"
engine = create_engine(DB_CONNECTION_STRING)

# Function to Fetch Unique States
def fetch_states():
    """
    Fetch distinct state names from the database.
    """
    query = "SELECT DISTINCT State_Name FROM bus_routes"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        states = [row[0] for row in result.fetchall()]
    return states

# Function to Fetch Unique Route Names for a Given State
def fetch_route_names(state_name):
    """
    Fetch distinct route names from the database based on the selected state.
    """
    query = "SELECT DISTINCT Route_Name FROM bus_routes WHERE State_Name = :state_name"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"state_name": state_name})
        routes = [row[0] for row in result.fetchall()]
    return routes

# Function to Fetch Unique Bus Types
def fetch_bus_types(route_name):
    """
    Fetch distinct bus types for a given route.
    """
    query = "SELECT DISTINCT Bus_Type FROM bus_routes WHERE Route_Name = :route_name"
    with engine.connect() as connection:
        result = connection.execute(text(query), {"route_name": route_name})
        bus_types = [row[0] for row in result.fetchall()]
    return bus_types

# Function to Fetch Filtered Data
def fetch_filtered_data(route_name, state_name=None, min_duration=None, max_duration=None, 
                         min_price=None, max_price=None, bus_type=None, 
                         min_star_rating=None, max_star_rating=None, 
                         min_seat_availability=None, max_seat_availability=None):
    """
    Fetch filtered bus data based on the provided filters.
    """
    query = "SELECT * FROM bus_routes WHERE Route_Name = :route_name"
    params = {"route_name": route_name}

    if state_name:
        query += " AND State_Name = :state_name"
        params["state_name"] = state_name

    if min_duration is not None and max_duration is not None:
        query += " AND Duration BETWEEN :min_duration AND :max_duration"
        params["min_duration"] = min_duration
        params["max_duration"] = max_duration

    if min_price is not None and max_price is not None:
        query += " AND Price BETWEEN :min_price AND :max_price"
        params["min_price"] = min_price
        params["max_price"] = max_price

    if bus_type:
        query += " AND Bus_Type = :bus_type"
        params["bus_type"] = bus_type

    if min_star_rating is not None and max_star_rating is not None:
        query += " AND Star_Rating BETWEEN :min_star_rating AND :max_star_rating"
        params["min_star_rating"] = min_star_rating
        params["max_star_rating"] = max_star_rating

    if min_seat_availability is not None and max_seat_availability is not None:
        query += " AND Seat_Availability BETWEEN :min_seat_availability AND :max_seat_availability"
        params["min_seat_availability"] = min_seat_availability
        params["max_seat_availability"] = max_seat_availability

    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        data = result.fetchall()

    columns = result.keys()
    df = pd.DataFrame(data, columns=columns)
    return df

# Function to Display Sidebar Filters
def display_sidebar_filters():
    """
    Display sidebar filters and return the selected filter values.
    """
    states = fetch_states()  # Fetch states from the database
    selected_state = st.sidebar.selectbox('Select State', [None] + states)

    selected_route = None
    if selected_state:
        route_names = fetch_route_names(selected_state)
        selected_route = st.sidebar.selectbox('Select Route Name', [None] + route_names)

    selected_bus_type = None
    if selected_route:
        bus_types = fetch_bus_types(selected_route)
        selected_bus_type = st.sidebar.selectbox('Filter by Bus Type', [None] + bus_types)

    # Duration Filter
    min_duration = st.sidebar.text_input('Min Duration (HH MM)', "00 15")
    max_duration = st.sidebar.text_input('Max Duration (HH MM)', "32 00")

    # Price Filter
    min_price = st.sidebar.number_input('Min Price', min_value=0, step=1, value=500)
    max_price = st.sidebar.number_input('Max Price', min_value=0, step=1, value=2000)

    # Star Rating Filter
    min_star_rating = st.sidebar.slider('Min Star Rating', min_value=1, max_value=5, step=1, value=1)
    max_star_rating = st.sidebar.slider('Max Star Rating', min_value=min_star_rating, max_value=5, step=1, value=5)

    # Seat Availability Filter
    min_seat_availability = st.sidebar.slider('Min Seat Availability (%)', min_value=0, max_value=100, step=1, value=0)
    max_seat_availability = st.sidebar.slider('Max Seat Availability (%)', min_value=min_seat_availability, max_value=100, step=1, value=100)

    filters = {
        "state_name": selected_state,
        "route_name": selected_route,
        "bus_type": selected_bus_type,
        "min_duration": min_duration,
        "max_duration": max_duration,
        "min_price": min_price if min_price > 0 else None,
        "max_price": max_price if max_price > 0 else None,
        "min_star_rating": min_star_rating,
        "max_star_rating": max_star_rating,
        "min_seat_availability": min_seat_availability,
        "max_seat_availability": max_seat_availability
    }

    return filters

# Main Function
def main():
    """
    Streamlit App for Redbus Data Filtering.
    """
    st.set_page_config(page_title="Red Bus Data", page_icon="🚌", layout="wide")

    st.title('🚌 Red Bus Data Scraping with Selenium & Dynamic Filtering using Streamlit')
    st.subheader("Filtered Bus Data Based on Route & Preferences")
    
    
    # Sidebar Filters
    filters = display_sidebar_filters()

    if filters["route_name"]:
        filtered_data = fetch_filtered_data(
            route_name=filters["route_name"],
            state_name=filters["state_name"],
            min_duration=filters["min_duration"],
            max_duration=filters["max_duration"],
            min_price=filters["min_price"],
            max_price=filters["max_price"],
            bus_type=filters["bus_type"],
            min_star_rating=filters["min_star_rating"],
            max_star_rating=filters["max_star_rating"],
            min_seat_availability=filters["min_seat_availability"],
            max_seat_availability=filters["max_seat_availability"]
        )

        st.write(f"### Filtered Data for Route: {filters['route_name']}")
        st.dataframe(filtered_data)
        st.image(r"C:\Users\Vishwa\Desktop\GUVI captone\REDBUS\logo.webp")

if __name__ == "__main__":
    main()
