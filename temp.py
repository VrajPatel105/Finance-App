import streamlit as st
import plost
import pandas as pd
import numpy as np

# Assuming you have a DataFrame with portfolio data
df = pd.DataFrame({
    'date': pd.date_range(start='2024-01-01', periods=100),
    'portfolio_value': [100000 + i*1000 + np.random.randn()*500 for i in range(100)]
})

st.title("Portfolio Performance")

plost.line_chart(
    data=df,
    x='date',
    y='portfolio_value',
    height=400,
    color='#1E88E5'
)
