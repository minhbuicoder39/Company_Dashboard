import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
from utils.utils import get_data_path

# Page config
st.set_page_config(page_title="China HRC Price", layout="wide")
st.title("*China HRC Daily Price*")

# Function to load and process HRC data
def load_hrc_data():
    df = pd.read_excel(get_data_path("china_hrc.xlsx"))
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Load data
try:
    df = load_hrc_data()
    # Filter last 3 months
    three_months_ago = datetime.now() - timedelta(days=90)
    df = df[df['Date'] >= three_months_ago]
    
    # Calculate moving averages
    df['MA5'] = df['Price_Yuan'].rolling(window=5).mean()
    df['MA20'] = df['Price_Yuan'].rolling(window=20).mean()

    # Create price chart
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(
        go.Scatter(
            x=df['Date'], 
            y=df['Price_Yuan'], 
            mode='lines', 
            name='Daily Price',
            line=dict(color='royalblue', width=2)
        )
    )
    
    # Add moving averages
    fig.add_trace(
        go.Scatter(
            x=df['Date'], 
            y=df['MA5'], 
            mode='lines', 
            name='5-day MA',
            line=dict(color='red', width=1, dash='dot')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['Date'], 
            y=df['MA20'], 
            mode='lines', 
            name='20-day MA',
            line=dict(color='green', width=1, dash='dot')
        )
    )

    # Update layout with better styling
    fig.update_layout(
        title={
            'text': "China HRC Price (Yuan/MT)",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Date",
        yaxis_title="Price (Yuan/MT)",
        template="plotly_white",
        height=600,
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Add range slider
    fig.update_xaxes(rangeslider_visible=True)
    
    st.plotly_chart(fig, use_container_width=True)

    # Display raw data in an expander
    with st.expander("Raw Data", expanded=False):
        st.dataframe(df)

except FileNotFoundError:
    st.error("Data file not found. Please ensure china_hrc.xlsx exists in the data directory.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

