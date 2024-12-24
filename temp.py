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
        
        self.conn.commit()
    
    def add_user(self, name, email, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor = self.conn.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?) RETURNING id',
                (name, email, hashed_password)
            )
            user_id = cursor.fetchone()[0]
            self.conn.commit()
            return user_id
        except:
            return None
    
    def verify_user(self, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor = self.conn.execute(
            'SELECT id, name, balance FROM users WHERE email=? AND password=?',
            (email, hashed_password)
        )
        result = cursor.fetchone()
        if result:
            return {'id': result[0], 'name': result[1], 'balance': result[2]}
        return None
    
    def get_portfolio(self, user_id):
        cursor = self.conn.execute(
            'SELECT symbol, shares, avg_price FROM portfolio WHERE user_id=?',
            (user_id,)
        )
        return cursor.fetchall()
    
    def update_portfolio(self, user_id, symbol, shares, price, is_buy):
        cursor = self.conn.execute(
            'SELECT shares, avg_price FROM portfolio WHERE user_id=? AND symbol=?',
            (user_id, symbol)
        )
        existing = cursor.fetchone()
        
        if is_buy:
            if existing:
                new_shares = existing[0] + shares
                new_avg_price = ((existing[0] * existing[1]) + (shares * price)) / new_shares
                self.conn.execute(
                    'UPDATE portfolio SET shares=?, avg_price=? WHERE user_id=? AND symbol=?',
                    (new_shares, new_avg_price, user_id, symbol)
                )
            else:
                self.conn.execute(
                    'INSERT INTO portfolio (user_id, symbol, shares, avg_price) VALUES (?, ?, ?, ?)',
                    (user_id, symbol, shares, price)
                )
        else:
            if existing and existing[0] >= shares:
                new_shares = existing[0] - shares
                if new_shares > 0:
                    self.conn.execute(
                        'UPDATE portfolio SET shares=? WHERE user_id=? AND symbol=?',
                        (new_shares, user_id, symbol)
                    )
                else:
                    self.conn.execute(
                        'DELETE FROM portfolio WHERE user_id=? AND symbol=?',
                        (user_id, symbol)
                    )
            else:
                return False
        
        # Record transaction
        self.conn.execute(
            'INSERT INTO transactions (user_id, symbol, transaction_type, shares, price) VALUES (?, ?, ?, ?, ?)',
            (user_id, symbol, 'BUY' if is_buy else 'SELL', shares, price)
        )
        
        # Update user balance
        transaction_value = shares * price
        self.conn.execute(
            'UPDATE users SET balance = balance + ? WHERE id=?',
            (-transaction_value if is_buy else transaction_value, user_id)
        )
        
        self.conn.commit()
        return True

def get_stock_data(symbol, period='1y'):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except:
        return None, None

def format_number(num):
    if abs(num) >= 1e9:
        return f'${num/1e9:.2f}B'
    elif abs(num) >= 1e6:
        return f'${num/1e6:.2f}M'
    elif abs(num) >= 1e3:
        return f'${num/1e3:.2f}K'
    else:
        return f'${num:.2f}'

def create_stock_chart(data, symbol):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    
    fig.update_layout(
        title=f'{symbol} Stock Price',
        yaxis_title='Price',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    
    return fig

def trading_page():
    st.title('Trading Dashboard')
    
    # Stock symbol input
    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL, GOOGL)', '').upper()
    
    if symbol:
        hist_data, stock_info = get_stock_data(symbol)
        
        if hist_data is not None and stock_info is not None:
            # Display stock info
            col1, col2, col3 = st.columns(3)
            current_price = hist_data['Close'].iloc[-1]
            
            with col1:
                st.metric(
                    label="Current Price",
                    value=f"${current_price:.2f}",
                    delta=f"{((current_price - hist_data['Close'].iloc[-2])/hist_data['Close'].iloc[-2]*100):.2f}%"
                )
            
            with col2:
                st.metric(
                    label="Market Cap",
                    value=format_number(stock_info.get('marketCap', 0))
                )
            
            with col3:
                st.metric(
                    label="Volume",
                    value=format_number(hist_data['Volume'].iloc[-1])
                )
            
            # Display chart
            st.plotly_chart(create_stock_chart(hist_data, symbol))
            
            # Trading form
            col1, col2 = st.columns(2)
            
            with col1:
                with st.form('buy_form'):
                    st.subheader('Buy Order')
                    shares_to_buy = st.number_input('Number of shares to buy', min_value=0.0, step=1.0)
                    total_cost = shares_to_buy * current_price
                    st.write(f'Total Cost: ${total_cost:.2f}')
                    buy_submitted = st.form_submit_button('Buy')
                    
                    if buy_submitted:
                        if total_cost > st.session_state.user['balance']:
                            st.error('Insufficient funds!')
                        else:
                            db = Database()
                            if db.update_portfolio(st.session_state.user['id'], symbol, shares_to_buy, current_price, True):
                                st.success(f'Successfully bought {shares_to_buy} shares of {symbol}')
                                st.session_state.user['balance'] -= total_cost
                                st.rerun()
                            else:
                                st.error('Transaction failed!')
            
            with col2:
                with st.form('sell_form'):
                    st.subheader('Sell Order')
                    shares_to_sell = st.number_input('Number of shares to sell', min_value=0.0, step=1.0)
                    total_value = shares_to_sell * current_price
                    st.write(f'Total Value: ${total_value:.2f}')
                    sell_submitted = st.form_submit_button('Sell')
                    
                    if sell_submitted:
                        db = Database()
                        if db.update_portfolio(st.session_state.user['id'], symbol, shares_to_sell, current_price, False):
                            st.success(f'Successfully sold {shares_to_sell} shares of {symbol}')
                            st.session_state.user['balance'] += total_value
                            st.rerun()
                        else:
                            st.error('Insufficient shares!')
        else:
            st.error('Invalid stock symbol or error fetching data')

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

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'user' not in st.session_state:
        st.session_state.user = None

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

def register_page(db):
    st.title('📝 Register New Account')
    
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
                    st.success('Registration successful! Please login.')
                    st.session_state.current_page = 'login'
                    st.rerun()
                else:
                    st.error('Registration failed. Email might already be registered.')

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
    
    # Initialize database
    db = Database()
    
    # Route to appropriate page based on session state
    if not st.session_state.logged_in:
        if st.session_state.current_page == 'register':
            register_page(db)
        else:
            login_page(db)
    else:
        create_sidebar()
        if st.session_state.current_page == 'portfolio':
            portfolio_page()
        else:
            trading_page()

if __name__ == "__main__":
    main()