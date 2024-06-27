import streamlit as st# type: ignore
import pandas as pd
import numpy as np
import yfinance as yf # type: ignore
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards # type: ignore
from streamlit_extras.grid import grid# type: ignore

st.title("Home broaker")

def build_sidebar():
    st.image("image/b3.png")

def build_main():
    pass


with st.sidebar:
    build_sidebar()