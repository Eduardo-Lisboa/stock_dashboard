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
        if len(tickers) == 1:
            prices = prices.to_frame()
            prices.columns = [tickers[0].replace(".SA","")]
        prices.columns = [t.replace(".SA","") for t in prices.columns]
        prices['IBOV'] = yf.download("^BVSP", start=start_date, end=end_date)["Adj Close"]
        return  tickers, prices
    return None, None

def build_main(tickers, prices):
    weights = np.ones(len(tickers))/len(tickers)
    prices['portfolio'] = prices.drop('IBOV', axis=1) @ weights
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
        elif t == "IBOV":
            colA.image("image/pie-chart-svgrepo-com.svg")
        else:
            colA.image(f'https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{t}.png', width=65)
        colB.metric(label="Retorno", value=f"{rets[t]:.0%}")
        colC.metric(label="Volatilidade", value=f"{vols[t]:.0%}")
        style_metric_cards(background_color='rgba(255,255,255,0)')

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("Desempenho Relativo")
        st.line_chart(norm_prices, height=600)

    with col2:
        st.subheader("Risco Retorno")
        fig = px.scatter(
            x=vols,
            y=rets,
            text=prices.columns,
            color=rets/vols,
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        
        fig.update_traces(
            textfont_color='white', 
            marker=dict(size=45),
            textfont_size=10,                  
        )
        fig.layout.yaxis.title = 'Retorno Total'
        fig.layout.xaxis.title = 'Volatilidade (anualizada)'
        fig.layout.height = 600
        fig.layout.xaxis.tickformat = ".0%"
        fig.layout.yaxis.tickformat = ".0%"        
        fig.layout.coloraxis.colorbar.title = 'Sharpe'
        st.plotly_chart(fig, use_container_width=True)

    
        


st.set_page_config(layout="wide")

with st.sidebar:
   tickers, prices = build_sidebar()

st.title("Para Investidores")
if tickers:
    build_main(tickers, prices)