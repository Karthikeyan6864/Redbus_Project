import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="redbus"
    )
    return connection
def convert_duration_to_minutes(duration_str):
    parts = duration_str.split(' ')
    total_minutes = 0
    for part in parts:
        if 'h' in part:  # Hours
            hours = int(part.replace('h', '').strip())
            total_minutes += hours * 60
        elif 'm' in part:  # Minutes
            minutes = int(part.replace('m', '').strip())
            total_minutes += minutes
    return total_minutes
def create_duration_ranges(filtered_df):
    """Creates continuous duration ranges based on the filtered DataFrame."""
    filtered_df['duration_minutes'] = filtered_df['duration'].apply(convert_duration_to_minutes)
    if filtered_df['duration_minutes'].empty:
        return filtered_df  

    min_duration = filtered_df['duration_minutes'].min()
    max_duration = filtered_df['duration_minutes'].max()

    bin_size = 60 
    bins = list(range(min_duration // bin_size * bin_size, (max_duration // bin_size + 1) * bin_size + 1, bin_size))

    labels = [f'{i}-{i + bin_size} mins' for i in bins[:-1]]

    filtered_df['duration_range'] = pd.cut(filtered_df['duration_minutes'], bins=bins, labels=labels, right=False)

    filtered_df['duration_range'] = filtered_df['duration_range'].astype(str)  # Ensure it's a string for sorting
    filtered_df.sort_values(by='duration_range', inplace=True)  # Sort by duration range

    return filtered_df

def fetch_data():
    connection = get_db_connection()
    query = "SELECT route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available FROM bus_data"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def categorize_bus_type(seat_value):
        seat_value = seat_value.lower()  # Convert to lower case for case insensitive matching
        if 'non' in seat_value and 'seater' in seat_value:
            return 'Non A/C Seater'
        elif 'non' in seat_value and 'sleeper' in seat_value:
            return 'Non A/C Sleeper'
        elif ('ac' in seat_value or 'a/c' in seat_value) and 'seater' in seat_value:
            return 'A/C Seater'
        elif ('ac' in seat_value or 'a/c' in seat_value) and 'sleeper' in seat_value:
            return 'A/C Sleeper'
        else:
            return 'Unknown' 

    


df = fetch_data()
df['bus_type'] = df['bustype'].apply(categorize_bus_type)

st.markdown(
    """
    <style>
    .header {
        background-image: url("https://images.unsplash.com/photo-1508614999368-9260051292e5?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 150px; /* Reduced header height */
        width: 100%;
        padding: 20px; /* Reduced padding */
        text-align: center;
        color: #FF5733; /* Updated font color (orange-red hex code) */
        font-size: 60px; /* Adjust font size */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="header">Redbus Project</div>', unsafe_allow_html=True)


tabs = st.sidebar.radio("Select a Tab", ["Home", "Dashboard"])



if tabs == "Home":
    st.markdown(
    """
    <style>
    .stSelectbox {
        text-align: left;
        width: 100%; /* Adjust the width of the selectboxes */
    }
    </style>
    """,
    unsafe_allow_html=True
    )
 
    options_Bus_route = df['route_name'].unique().tolist()

    
    col1, col2 = st.columns(2)
    with col1:
        selected_Bus_route = st.selectbox("Select bus route (Step 1)", options_Bus_route)
    
    
    filtered_df_1 = df[df['route_name'] == selected_Bus_route]

    with col2:
       
        options_Bus_type = filtered_df_1['bus_type'].unique().tolist()
        selected_Bus_type = st.selectbox("Select bus type (Step 2)", options_Bus_type)

    
    filtered_df_2 = filtered_df_1[filtered_df_1['bus_type'] == selected_Bus_type]

   
    col3, col4 = st.columns(2)
    with col3:
        
        options_Rating = filtered_df_2['star_rating'].unique().tolist()
        selected_Rating = st.selectbox("Select Ratings (Step 3)", options_Rating)

   
    filtered_df_3 = filtered_df_2[filtered_df_2['star_rating'] == selected_Rating]

    with col4:
        
        options_Duration = filtered_df_3['duration'].unique().tolist()
        selected_Duration = st.selectbox("Select Duration (Step 4)", options_Duration)

    
    final_filtered_df = filtered_df_3[filtered_df_3['duration'] == selected_Duration]

    
    st.write(f"You selected {selected_Bus_route}, {selected_Bus_type}, {selected_Rating}, {selected_Duration}")

   
    if final_filtered_df.empty:
        st.write("No records found for the selected criteria.")
    else:
        st.write("Filtered Data:")
        columns_to_display = ['busname', 'price', 'seats_available', 'departing_time', 'reaching_time', 'route_link']
        st.dataframe(final_filtered_df[columns_to_display])
elif tabs == "Dashboard":
    bus_route_options = df['route_name'].unique().tolist()
    selected_route = st.selectbox("Select Bus Route", bus_route_options)


    filtered_df= df[df['route_name'] == selected_route]


    if filtered_df.empty:
          
        st.write("No data available for the selected bus route.")
    else:
        
        col1, col2 = st.columns(2)

        with col1:
            
            bus_type_counts = filtered_df['bus_type'].value_counts()
            colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']


            fig = go.Figure(data=[go.Pie(labels=bus_type_counts.index,
                             values=bus_type_counts.values)])
            fig.update_traces(hoverinfo='label+percent', 
                              textinfo='value', 
                              textfont_size=20,
                              marker=dict(colors=colors, line=dict(color='#000000', width=2)))

            fig.update_layout(title_text="Bus Type Distribution", title_font_size=24)
            st.plotly_chart(fig)

        with col2:
            st.subheader("Scatter Plot: Price vs Star Rating by Bus Type")
            fig2 = px.scatter(filtered_df, 
                      y="price", 
                      x="star_rating", 
                      color="bus_type", 
                      title="Price vs Star Rating by Bus Type")
            fig2.update_traces(marker_size=10)
            fig2.update_layout(scattermode="group", 
                               scattergap=0.75, 
                               xaxis_title="Star Rating", 
                               yaxis_title="Price")

            st.plotly_chart(fig2)

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Bar Plot: Average Price by Bus Type")

            avg_price_df = filtered_df.groupby('bus_type', as_index=False)['price'].mean()

            fig3 = px.bar(avg_price_df, x='bus_type', y='price', color='bus_type', barmode='group',
                         labels={"price": "Average Price", "bus_type": "Bus Type"})

    
            fig3.update_layout(yaxis_tickformat='.0f') 
            st.plotly_chart(fig3)

        with col4:
            filtered_df = create_duration_ranges(filtered_df)
            if filtered_df.empty:
                st.write("No data available for the selected criteria after creating duration ranges.")
            else:
                fig4 = px.histogram(filtered_df, 
                                    x='duration_range', 
                                    y='seats_available',  
                                    title='Histogram: Seats available by Duration Ranges',
                                    labels={"seats_available": "Seats available", "duration_range": "Duration Ranges"},
                                    histfunc='count',  
                                    color='duration_range')  

                fig4.update_layout(
                                    xaxis_title="Duration Ranges",
                                    yaxis_title="Seats available",
                                    xaxis=dict(
                                               categoryorder='array',
                                               categoryarray=sorted(
                                               filtered_df['duration_range'].unique(), 
                                               key=lambda x: (int(x.split('-')[0].strip()), int(x.split('-')[1].split()[0].strip()))  # Remove 'mins' and split by '-'
                                                )
                                                )
                                                )

                st.plotly_chart(fig4)



