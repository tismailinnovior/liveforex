import streamlit as st
from sqlalchemy import text, create_engine
from os import environ
import psycopg2
import yfinance as yf
import pandas as pd
from datetime import date
from datetime import datetime

st.title("S&P/ASX 200 MARKET DATA")


#get the forex info
ticker_obj = yf.Ticker('^AXJO')
info_dict = ticker_obj.info
#info_dict.keys()
#add extra metric
info_dict['fiftyTwoWeekRange'] = str(info_dict['fiftyTwoWeekLow']) + " - " + str(info_dict['fiftyTwoWeekHigh'])



#Display metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("DAY HIGH", info_dict['dayHigh'])
with col2:
    st.metric("DAY LOW", info_dict['dayLow'])
with col3:
   st.metric("PRE CLOSE", info_dict['previousClose'])
with col4:
    st.metric("52 WEEKS RANGE", info_dict['fiftyTwoWeekRange'])

#Download Market data

#Choose Ticker, Period and interval for data download
c1, c2,c3 = st.columns(3)
with c1:
    ticker_symbol = st.selectbox("Select Ticker",
         options = ["GOOG", "SPY","^AXJO" ])
with c2:
    target_period = st.selectbox("Select Period",
         options = ["1d", "5d","1mo"])
with c3:
    data_interval = st.selectbox("Select Interval",
         options = ["5m", "15m","30m","60m"])

fx_data = yf.download(tickers = ticker_symbol ,period = target_period, interval = data_interval)

#Format columns
cols_name =['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
fx_data = fx_data.set_axis(cols_name, axis=1)
fx_data = fx_data.reset_index()
fx_data['Date'] = pd.to_datetime(fx_data['Datetime']).dt.date
cols_reorder =['Datetime', 'Date','Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
fx_data = fx_data[cols_reorder]
#display dataframe
st.dataframe(fx_data, use_container_width=True)

# line chart
st.line_chart(data = fx_data, x= "Date", y = "Adj Close")