import streamlit as st
import pandas as pd

# Load the large DataFrame without displaying it
@st.cache_data
def load_data():
    return pd.read_csv("all_stock_data.csv", parse_dates=["Date"])

df = load_data()

# Streamlit UI
st.title("Stock Price Lookup")

# User input for company name
company_name = st.text_input("Enter Company Name (e.g., 삼성전자)", "").strip()

# Multi-date selection
available_dates = df["Date"].dt.strftime('%Y-%m-%d').unique()
selected_dates = st.multiselect("Select Dates", available_dates)

# Convert selected dates back to datetime format
selected_dates = pd.to_datetime(selected_dates)

# Button to confirm selection
proceed = st.button("Proceed")

# Search and Display only when the button is pressed
if proceed and company_name and not selected_dates.empty:
    result = df[(df["name"] == company_name) & df["Date"].isin(selected_dates)]

    if not result.empty:
        st.write("### Stock Data for Selected Dates")
        st.dataframe(result[["Date", "Open", "High", "Low", "Close", "Volume"]])
    else:
        st.error("No data found for the selected company and dates.")