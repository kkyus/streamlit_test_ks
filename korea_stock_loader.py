
import pandas as pd
from pykrx import stock
import streamlit as st 


def get_historical_data(start_date, end_date):
    kospi_tickers = stock.get_market_ticker_list(market="KOSPI")[:5]
    kosdaq_tickers = stock.get_market_ticker_list(market="KOSDAQ")[:5]

    dataframes = []
    tickers = pd.DataFrame({
        'ticker': kospi_tickers + kosdaq_tickers,
        'market': ['KOSPI'] * len(kospi_tickers) + ['KOSDAQ'] * len(kosdaq_tickers)
    })

    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    total_tickers = len(tickers)
    progress_bar = st.progress(0)
    progress_text = st.empty()

    for idx, row in enumerate(tickers.iterrows()):
        ticker = row[1]['ticker']
        market = row[1]['market']
        
        df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
        df['ticker'] = ticker
        df['market'] = market
        dataframes.append(df)
        
        # Update the progress bar
        progress = (idx + 1) / total_tickers
        progress_bar.progress(progress)
        progress_text.write(f"Progress: {idx + 1}/{total_tickers}")

    whole_dataframe = pd.concat(dataframes)
    whole_dataframe.reset_index(inplace=True)
    whole_dataframe['날짜'] = whole_dataframe['날짜'].dt.strftime('%Y-%m-%d')

    return whole_dataframe

def show():
    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")
    
    if 'historical_data' not in st.session_state:
        st.session_state.historical_data = None

    if st.button('Get historical data'):
        with st.spinner('Fetching data...'):
            st.session_state.historical_data = get_historical_data(start_date, end_date)
            st.success('Data fetched successfully!')
            st.dataframe(st.session_state.historical_data.head())

    if st.session_state.historical_data is not None:
        dataframe = st.session_state.historical_data.to_csv(index = False).encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=dataframe,
            file_name="korea_stock_data.csv",
            mime="text/csv",
        )

show()
