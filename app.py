

'''
Vraj Patel and Jaikishan Patel

Trading Platform: A Comprehensive Stock Trading Web Application

This innovative trading platform, is a sophisticated Streamlit-based web application designed to provide users with a comprehensive stock trading experience.

The application offers a range of features including:
                        Real-time stock market data retrieval
                        User authentication and registration
                        Portfolio tracking and management
                        Interactive stock trading functionality
                        Detailed stock price visualization
Key Technologies Used:
                        Streamlit for web interface
                        YFinance for live stock data
                        SQLite for database management
                        Plotly for interactive charting
                        Hashlib for secure password hashing
The platform enables users to:
                        Create and manage personal trading accounts
                        Buy and sell stocks in real-time
                        Track portfolio performance
                        View detailed stock information and historical price charts

'''

import streamlit as st
import yfinance as yf # to get live data 
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib # for hashing the password
import sqlite3 # for database
import plotly.graph_objects as go # to plot candlestick chart


# class dastabase
class Database:
    def __init__(self):
        # sqllite3 is a lightweight database
        # sqlite.connect will connect to the trading_app.db and if this dosent exist it will create a new one.
        # self.conn This stores the database connection as an instance variable

        self.conn = sqlite3.connect('trading_app.db', check_same_thread=False) # on calling self.conn, it will connect to the trading_app.db database. and if it dosent exist's it will create a new one 
        self.create_tables() # calling the function

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
        
         #   Explaination of the above table:
         #   self.conn.execute -> this will simply make a connection to the sql lite database
         #   PRIMARY KEY -> A universal value. This of it as someone's passport number.
         #   AUTOINCREMENT -> the id will initially start from 1 and than will be incremented automatically
         #   email -> should be a unique text inside the database.
         #   balance is a real number 
         #   DEFAULT is the value that all the users will get from the very start
        
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

       # \* FOREIGN KEY -> Here you are establishing a connection from the users table 'id' and referencing it to foreign key. *\
        
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

    # Function for adding a new user into the database
    def add_user(self,name, email, password):
        try:
            # Hashing the password to improve account security.
            # sha256 encoding cannot be reversed.
            hashed_password = hashlib.sha256(password.encode()).hexdigest() 

            cursor = self.conn.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?) RETURNING id', 
                (name, email, hashed_password)
            )

            ''' Here the cursor is an object. When self.conn.execute is executed, it will return
            an object that contains the RETURNING id. And then we will use fetchone function to
            fetch the id contained inside the cursor object.
            '''

            user_id = cursor.fetchone()[0] # this fetchone will fetch the things contained inside the cursor object
            self.conn.commit() # Same as github. We need to commit the changes to the server
            return user_id
        except:
            return None

    # Function to verify the user by matching the password present in the database and the password entered by the user. 
    # Here since sha256 encoding is not reversible, to check the password, we are converting the password that entered 
    # by the user and checking the hashed password with the original hashed password stored in the database
    def verify_user(self, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        returned_id = self.conn.execute(
            ' SELECT id, name, balance FROM users WHERE email=? AND password=?', 
            (email, hashed_password)
        )

        result = returned_id.fetchone() 

        '''
        fetchone():
        Returns a single row or record from the query result
        Moves the cursor position by one row each time it's called

        fetchall():
        Retrieves all remaining rows from the query result set
        Returns a list of tuples, with each tuple representing a row
        ''' 

        if result: 
            return {'id': result[0], 'name': result[1], 'balance': result[2]}
        else:
            return None
        
    # Function to get the portfolio for the user . Here we are fetching the data from the database by searching it based on the user id.
    def get_portfolio(self, user_id):
        cursor = self.conn.execute(
            'SELECT symbol, shares, avg_price FROM portfolio WHERE user_id=?',
            (user_id,)
        )
        return cursor.fetchall()

    # Function to update the portfolio. When a user buys or sells a stock, update_portfolio function is called to change the user's portfolio .
    def update_portfolio(self,user_id, symbol, shares, price, is_buy):
        # Here the is_buy is a boolean. If it's a buy, then is_buy = True else False.
        cursor = self.conn.execute(
            'SELECT shares, avg_price FROM portfolio WHERE user_id = ? AND symbol=?',
            (user_id,symbol)
        )
        existing = cursor.fetchone()
        # We are storing the row into existing named list. 
        # If the user has buyed an existing stock's , then the existing list will contain that stock and the below 
        # if statement will be executed meaning that the stock values will be changed in the user's portfolio 
        # But if it's a complete new stock, then it will not be contained by the existing list, so the else condition will be called and a new stock will be added into the user's portfolio
        if is_buy:
            if existing:
                new_shares = existing[0] + shares # existing is a list with elements [current_shares, avg_price]. Therefore existing[0] gives the current number of shares.
                only_new_share_avg_price = shares * price # caluculating the new price only for the stocks that were bought latest
                new_avg_price = ((existing[0] + only_new_share_avg_price)) / new_shares # Calculating the average

                # Updating the portfolio
                self.conn.execute(
                    'UPDATE portfolio SET shares=?, avg_price=? WHERE user_id=? AND symbol=?',
                    (new_shares, new_avg_price, user_id, symbol)
                )
            else:
                self.conn.execute(
                    'INSERT INTO portfolio (user_id, symbol, shares, avg_price) VALUES (?, ?, ?, ?)',
                    (user_id,symbol,shares,price)
                )

        # If the order is for selling
        else:
            # If it's an existing stock already inside our database and the shares bought are less than the shares that the user wants to sell
            if existing and existing[0] >= shares:
                new_shares = existing[0] - shares
                # checking if the new shares are not less than 0 and if it is than delete entire stock row as the stock is no more inside the user's portfolio
                if new_shares > 0:
                    self.conn.execute(
                        'UPDATE portfolio SET shares=? WHERE user_id=? AND symbol=?',
                        (new_shares, user_id, symbol)
                        )
                else:
                    # Deleting the entire row for that particular user's particular stock
                    self.conn.execute(
                        'DELETE FROM portfolio WHERE user_id = ? AND symbol=?',(user_id,symbol)
                    )
            else:
                # Returning false if the stock is not existing in the database. Since if there's no stock bought, it cannot be sold in the first place
                return False


        # recording the transaction
        self.conn.execute(
            'INSERT INTO transactions (user_id, symbol, transaction_type, shares, price) VALUES (?, ?, ?, ?, ?)',
            (user_id,symbol,'BUY' if is_buy else 'SELL', shares, price)
        )


        # updating the user's balance
        transaction_value = shares * price
        self.conn.execute(
            'UPDATE users SET balance = balance + ? WHERE id=?',
            (-transaction_value if is_buy else transaction_value, user_id)
        )

        self.conn.commit()
        return True


# Function to load Registration page
def register_page(db):
    st.title('Register New Account')

    # form to register a new user
    with st.form('register_form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        submitted = st.form_submit_button('Register')

    # if the submitted button is pressed
    if submitted:
        # If both password matches
        if password != confirm_password:
            st.error('Passwords do not match')
        # if all the fields are entered
        elif not all([name, email, password]):
            st.error('All fields are required')
        else:
            # Calling the add_user function from the database class
            user_id = db.add_user(name, email, password)
            if user_id:
                st.success('Registration successful! Please Login.')
                st.session_state.current_page = 'login'
                st.rerun()
            else:
                st.error('Registration failed. Email might already be registered.')


# Function to get the live data from the the market using yfinance api
def get_stock_data(symbol, period='1y'):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info # This will return history of the stock. hist will be a "''DataFrame''". Info will be a dictionary
    except:
        return None, None

# Function to load the login page
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
        st.session_state.current_page = 'register' # If the register new account button is clicked, the page will be loaded to register page.
        st.rerun()

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    if 'user' not in st.session_state:
        st.session_state.user = None

# A simple Function for loading the welcome page.
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
    # A chart on the welcome page
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
            title="Trade Easily and Securely",
            yaxis_title="Stock Price",
            template="plotly_dark",
            height=400
        )
    
        st.plotly_chart(fig, use_container_width=True)


# Function for loading the portfolio page once user is logged in
def portfolio_page():
    st.title('Portfolio Overview')
    
    db = Database() # Creating an instance of the class Database
    portfolio = db.get_portfolio(st.session_state.user['id']) # calling the get_portfolio function inside the database which will return the portfolio of that user.
                                                            # portfolio will contain a list of tuples, with each tuple representing a row
    
    if portfolio:
        # Create portfolio dataframe
        portfolio_data = []
        total_value = 0 # Initial value of the portfolio
        
        for symbol, shares, avg_price in portfolio: # Iterating through the tuples for each row
             # calling the get_stock_data function to get the data from yfinance. 
            hist_data, _ = get_stock_data(symbol, period='1d') # Here hist_data is the history returned ( DataFrame format) and
                                                                # the _ means that the function is returning the dict but we dont want to use it here. So we simply ignore it
            if hist_data is not None:
                current_price = hist_data['Close'].iloc[-1] # Getting the last closing price using the -1 index
                # calculating the values
                position_value = shares * current_price
                total_value += position_value
                profit_loss = (current_price - avg_price) * shares
                profit_loss_pct = ((current_price - avg_price) / avg_price) * 100 # Percentage 
                
                # Adding the vlues inside the portfolio_data list. 
                portfolio_data.append({
                    'Symbol': symbol,
                    'Shares': shares,
                    'Avg Price': f'${avg_price:.2f}', # .2f is format speciffier on how to display the floating point number
                    'Current Price': f'${current_price:.2f}',
                    'Value': f'${position_value:.2f}',
                    'Profit/Loss': f'${profit_loss:.2f} ({profit_loss_pct:.2f}%)'
                })
        
        # If there is any data in the portfolio_data list then we are using the pd.DataFrame function from stremalit and displaying the values in form of dataframe
        if portfolio_data:
            st.dataframe(pd.DataFrame(portfolio_data))
            st.metric(
                label="Total Portfolio Value",
                value=f'${total_value:.2f}',
                delta=f'${total_value - 100000:.2f}'
            )
    else:
        st.info('Your portfolio is empty. Start trading to build your portfolio!')

# Function to format the big numbers into Billion, Million and Thousand Format
def format_number(num):
    if abs(num) >= 1e9:
        return f'${num/1e9:.2f}B'
    elif abs(num) >= 1e6:
        return f'${num/1e6:.2f}M'
    elif abs(num) >= 1e3:
        return f'${num/1e3:.2f}K'
    else:
        return f'${num:.2f}'

# Function for creating a candelstick chart
def create_stock_chart(data, symbol):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])  #Here the open, high, low and close are inbuild functiosn offered by plotly. 

     # To update the layout
    fig.update_layout(
        title=f'{symbol} Stock Price',
        yaxis_title='Price',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    # this will return the plotted figure
    return fig

# Function for loading the trading page
def trading_page():
    st.title('Trading Dashboard')
    
    # Stock symbol input
    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL, GOOGL)', '').upper()

    if symbol:
        hist_data, stock_info = get_stock_data(symbol) # calling the function get_stock_data by the argument symbol
        # hist_data is a Dataframe and stock_info is a dictionary

        if hist_data is not None and stock_info is not None:
            # Display stock info
            col1, col2, col3 = st.columns(3)
            current_price = hist_data['Close'].iloc[-1]
            
            # Displaying the stock's values that were fetched from yfinance using the get_stock_data function
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

            # for buying the stock
            with col1:
                with st.form('buy_form'):
                    st.subheader('Buy Stock')
                    shares_to_buy = st.number_input('Number of shares to buy', min_value=0.0, step=1.0)
                    total_share_cost = shares_to_buy * current_price
                    st.write(f'Total Cost: ${total_share_cost:.2f}')
                    buy_submit_btn = st.form_submit_button('Buy')

                    if buy_submit_btn:
                        # Fetching the user's balance to check if the user has enough funds to buy the shares if not than error
                        if total_share_cost > st.session_state.user['balance']:
                            st.error('Insufficient funds!')
                        else:
                            # If the user has enough funds
                            db = Database()
                            # Calling the update_portfolio function from the database with the argments as the user's id symbol, shares, current_price, and if it's a buy or a sell
                            if db.update_portfolio(st.session_state.user['id'],symbol,shares_to_buy,current_price, True):
                                st.success(f'Successfully bought {shares_to_buy} shares of {symbol}')
                                st.session_state.user['balance'] -= total_share_cost # substracting the amount from the user's total balance
                                st.rerun()
                            else:
                                st.error('Transaction Failed. Please try later') # else Failed
            

            # for selling the stock
            with col2:
                with st.form('sell_form'):
                    st.subheader('Sell Stock')
                    shares_to_sell = st.number_input('Number of shares to sell', min_value=0.0, step=1.0)
                    total_share_cost_for_selling = shares_to_sell * current_price
                    st.write(f'Total Cost : ${total_share_cost:.2f}')
                    sell_submit_btn = st.form_submit_button('Sell')

                    if sell_submit_btn:
                        db = Database()
                        # Firstly checking if the user has enough shares to sell. If not then error
                        if db.update_portfolio(st.session_state.user['id'],symbol,shares_to_sell,current_price,False):
                            st.success(f'Successfully Sold {shares_to_sell} shares of {symbol}') # User had shares for that stocks so sell 
                            st.session_state.user['balance'] += total_share_cost_for_selling
                            st.rerun()
                        else:
                            st.error('Insufficient amount of Shares') # else failed
        else:
            st.error('Invalid stock symbol or error fetching the data. Please try again Later.')

# Function to load a side bar containing a portfolio, trade and logout button
def create_sidebar():
    with st.sidebar:
        st.title('Navigation')
        st.write(f"Welcome, {st.session_state.user['name']}!")
        st.metric(
            label="Available Balance",
            value=f"${st.session_state.user['balance']:.2f}",
            delta=f"${st.session_state.user['balance'] - 100000:.2f}"
        )
        
        # checking which button is pressed and changing the current page based on that
        if st.button('📊 Portfolio'):
            st.session_state.current_page = 'portfolio'
        if st.button('💱 Trade'):
            st.session_state.current_page = 'trading'
        
        st.sidebar.button('🚪 Logout', on_click=logout) # if it's clicked, it will call the logout function


# Function to logout
def logout():
    st.session_state.logged_in = False
    st.session_state.current_page = 'login'
    st.session_state.user = None # This will forget the user

# main
def main():
    st.set_page_config(
        page_title="Trading Platform",
        page_icon="📈",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()

    db = Database() # An instance of Database class

    if not st.session_state.logged_in:
        if st.session_state.current_page == 'welcome':
            welcome_page()
        elif st.session_state.current_page == 'register':
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