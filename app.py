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

    def add_user(self,name, email, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor = self.conn.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?) RETURNING id', (name, email, hashed_password)
            )

            ''' Here the cursor is an object. When self.conn.execute is executed, it will return
            an object that contains the RETURNING id. And then we will use fetchone function to
            fetch the id contained inside the cursor object.
            '''

            user_id = cursor.fetchone()[0]
            self.conn.commit()
            return user_id
        except:
            return None

    def verify_user(self, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        returned_id = self.conn.execute(
            ' SELECT id, name, balance FROM users WHERE email=? AND password=?', (email, hashed_password)
        )

        result = returned_id.fetchone()
        if result: 
            return {'id': result[0], 'name': result[1], 'balance': result[2]}
        else:
            return None
        

    def get_portfolio(self, user_id):
        cursor = self.conn.execute(
            'SELECT symbol, shares, avg_price FROM portfolio WHERE user_id=?',
            (user_id,)
        )
        return cursor.fetchall()


def register_page(db):
    st.title('Register New Account')

    with st.form('register_form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        submitted = st.form_submit_button('Register')

    if submitted:
        if password != confirm_password:
            st.error('Passwords do not match')
        elif not all([name, email, password]):
            st.error('All fields are required')
        else:
            user_id = db.add_user(name, email, password)
            if user_id:
                st.success('Registration successful! Please Login.')
                st.session_state.current_page = 'login'
                st.rerun()
            else:
                st.error('Registration failed. Email might already be registered.')



def get_stock_data(symbol, period='1y'):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except:
        return None, None




def login_page(db):
    st.title('📈 Trading Platform')
    
    with st.form('login_form'):
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Login')

        if submitted:
            user = db.verify_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.current_page = 'trading'
                st.rerun()
            else:
                st.error('Invalid email or password')
    
    if st.button('Register New Account'):
        st.session_state.current_page = 'register'
        st.rerun()

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    if 'user' not in st.session_state:
        st.session_state.user = None


def welcome_page():
    st.title("Welcome to Trading Platform 📈")
    
    # Create a two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Start Your Trading Journey Today!
        
        Our platform offers:
        * Real-time market data
        * Portfolio tracking
        * Historical price analysis
        * User-friendly interface
        
        Join thousands of traders who trust our platform for their investment needs.
        """)
        
        # Add login and register buttons
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("Login", type="primary", use_container_width=True):
                st.session_state.current_page = 'login'
                st.rerun()
        with col1_2:
            if st.button("Register", use_container_width=True):
                st.session_state.current_page = 'register'
                st.rerun()
    
    with col2:
        # Create a sample chart for visualization
        fig = go.Figure(data=[go.Candlestick(
            x=['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
            open=[100, 102, 104, 101, 105],
            high=[104, 107, 108, 105, 108],
            low=[99, 100, 101, 99, 102],
            close=[102, 104, 101, 105, 107]
        )])
        
        fig.update_layout(
            title="Sample Trading Chart",
            yaxis_title="Stock Price",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)



def portfolio_page():
    st.title('Portfolio Overview')
    
    db = Database()
    portfolio = db.get_portfolio(st.session_state.user['id'])
    
    if portfolio:
        # Create portfolio dataframe
        portfolio_data = []
        total_value = 0
        
        for symbol, shares, avg_price in portfolio:
            hist_data, _ = get_stock_data(symbol, period='1d')
            if hist_data is not None:
                current_price = hist_data['Close'].iloc[-1]
                position_value = shares * current_price
                total_value += position_value
                profit_loss = (current_price - avg_price) * shares
                profit_loss_pct = ((current_price - avg_price) / avg_price) * 100
                
                portfolio_data.append({
                    'Symbol': symbol,
                    'Shares': shares,
                    'Avg Price': f'${avg_price:.2f}',
                    'Current Price': f'${current_price:.2f}',
                    'Value': f'${position_value:.2f}',
                    'Profit/Loss': f'${profit_loss:.2f} ({profit_loss_pct:.2f}%)'
                })
        
        if portfolio_data:
            st.dataframe(pd.DataFrame(portfolio_data))
            st.metric(
                label="Total Portfolio Value",
                value=f'${total_value:.2f}',
                delta=f'${total_value - 100000:.2f}'
            )
    else:
        st.info('Your portfolio is empty. Start trading to build your portfolio!')


def trading(self):
    pass



def create_sidebar():
    with st.sidebar:
        st.title('Navigation')
        st.write(f"Welcome, {st.session_state.user['name']}!")
        st.metric(
            label="Available Balance",
            value=f"${st.session_state.user['balance']:.2f}",
            delta=f"${st.session_state.user['balance'] - 100000:.2f}"
        )
        
        if st.button('📊 Portfolio'):
            st.session_state.current_page = 'portfolio'
        if st.button('💱 Trade'):
            st.session_state.current_page = 'trading'
        
        st.sidebar.button('🚪 Logout', on_click=logout)


def logout():
    st.session_state.logged_in = False
    st.session_state.current_page = 'login'
    st.session_state.user = None
    st.rerun()


def main():
    st.set_page_config(
        page_title="Trading Platform",
        page_icon="📈",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()

    db = Database()

    if not st.session_state.logged_in:
        if st.session_state.current_page == 'welcome':
            welcome_page()
        elif st.session_state.current_page == 'register':
            register_page(db)
        else:
            login_page(db)
    else:
        create_sidebar()




if __name__ == "__main__":
    main()