import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib
import sqlite3
import plotly.graph_objects as go



class Database:
    def __init__(self):
        # sqllite3 is a lightweight database
        # sqlite.connect will connect to the trading_app.db and if this dosent exist it will create a new one.
        # self.conn This stores the database connection as an instance variable

        self.conn = sqlite3.connect('trading_app.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        # Users table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 100000.0
        )''')
        
        # Portfolio table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT NOT NULL,
            shares REAL NOT NULL,
            avg_price REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        
        # Transactions table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            shares REAL NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        
        self.conn.commit() # commit -> establishes connection




def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'user' not in st.session_state:
        st.session_state.user = None



def main():
    st.set_page_config(
        page_title="Trading Platform",
        page_icon="📈",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()


    db = Database()

