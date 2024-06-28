import streamlit as st# type: ignore
import pandas as pd
import numpy as np
import yfinance as yf # type: ignore
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards # type: ignore
from streamlit_extras.grid import grid# type: ignore


def build_sidebar():
    st.image("image/b3.png")
    tickler_list = pd.read_csv("tickers_ibra.csv",index_col=0)
    tickers = st.multiselect("Escolha os ativos", options=tickler_list,placeholder="Selecione os ativos")
    tickers = [t+".SA" for t in tickers]
    start_date = st.date_input("Data de inicio", format="DD/MM/YYYY", value=datetime(2021,1,1))
    end_date = st.date_input("Data de fim", format="DD/MM/YYYY", value="today", )

    if tickers:
        prices = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
        prices.columns = [t.replace(".SA","") for t in prices.columns]
        return  tickers, prices
    return None, None

def build_main(tickers, prices):
    weights = np.ones(len(tickers))/len(tickers)
    prices['portfolio'] = prices @ weights
    norm_prices = 100*prices/prices.iloc[0]
    returns = prices.pct_change()[1:]
    vols    = returns.std()*np.sqrt(252)
    rets = (norm_prices.iloc[-1] - 100)/100

    mygrid = grid( 5 ,5 ,5 ,5 ,5 , 5, vertical_align="top")
    for t in prices.columns:
        c = mygrid.container(border=True)
        c.subheader(t, divider="blue")
        colA, colB, colC = c.columns(3)
        if t == "portfolio":
            colA.image("image/pie-dollar.svg")
        else:
            colA.image(f'https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{t}.png', width=65)
        colB.metric(label="Retorno", value=f"{rets[t]:.0%}")
        colC.metric(label="Volatilidade", value=f"{vols[t]:.0%}")
        style_metric_cards(background_color='rgba(255,255,255,0)')

    
        


st.set_page_config(layout="wide")

with st.sidebar:
   tickers, prices = build_sidebar()

st.title("Para Investidores")
if tickers:
    build_main(tickers, prices)