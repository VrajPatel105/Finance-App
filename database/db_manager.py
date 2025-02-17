import sqlite3
import streamlit as st
import json
import hashlib

class Database:
    def __init__(self):
        # sqllite3 is a lightweight database
        # sqlite.connect will connect to the trading_app.db and if this dosent exist it will create a new one.
        # self.conn This stores the database connection as an instance variable
        self.conn = sqlite3.connect('trading_app.db', check_same_thread=False)  # on calling self.conn, it will connect to the trading_app.db database. and if it dosent exist's it will create a new one 
        self.create_tables()  # calling the function


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

        # FOREIGN KEY -> Here you are establishing a connection from the users table 'id' and referencing it to foreign key.
        
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

    
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS crypto_portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT NOT NULL,
            crypto_amount REAL NOT NULL,
            avg_price REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS location_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            city TEXT,
            region TEXT,
            country TEXT,
            timezone TEXT,
            device TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')

        self.conn.commit()  # commit -> establishes connection


# Add these methods to Database class
    def log_location(self, user_id, location_data):
        """Log user's location with timestamp"""
        try:
            self.conn.execute('''
                INSERT INTO location_history 
                (user_id, city, region, country, timezone, device) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                location_data['city'],
                location_data['region'],
                location_data['country'],
                location_data['timezone'],
                location_data.get('device', 'Unknown')
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error logging location: {e}")
            return False

    def get_location_history(self, user_id, limit=5):
        """Get user's recent location history"""
        cursor = self.conn.execute('''
            SELECT city, region, country, timezone, device, timestamp
            FROM location_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        return cursor.fetchall()
    
    
    def verify_and_sync_balance(self, user_id):
        """Verify and sync the database balance with session state"""
        cursor = self.conn.execute('SELECT balance FROM users WHERE id=?', (user_id,))
        db_balance = cursor.fetchone()[0]
        
        # If session state balance doesn't match database, update it
        if st.session_state.user['balance'] != db_balance:
            st.session_state.user['balance'] = db_balance
            
            # Update query parameters
            state_data = {
                'logged_in': st.session_state.logged_in,
                'current_page': st.session_state.current_page,
                'user': st.session_state.user
            }
            st.query_params['session_state'] = json.dumps(state_data)
        
        return db_balance


    # Function for adding a new user into the database
    def add_user(self, name, email, password):
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

            user_id = cursor.fetchone()[0]  # this fetchone will fetch the things contained inside the cursor object
            self.conn.commit()  # Same as github. We need to commit the changes to the server
            return user_id
        except:
            return None

    # Function to verify the user by matching the password present in the database and the password entered by the user. 
    # Here since sha256 encoding is not reversible, to check the password, we are converting the password that entered 
    # by the user and checking the hashed password with the original hashed password stored in the database
    def verify_user(self, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        returned_id = self.conn.execute(
            'SELECT id, name, balance, email FROM users WHERE email=? AND password=?',
            (email, hashed_password)
        )

        result = returned_id.fetchone()

        # fetchone():
        # Returns a single row or record from the query result
        # Moves the cursor position by one row each time it's called

        # fetchall():
        # Retrieves all remaining rows from the query result set
        # Returns a list of tuples, with each tuple representing a row

        if result:
            return {'id': result[0], 'name': result[1], 'balance': result[2], 'email': result[3]}
        else:
            return None

    # Function to get the portfolio for the user . Here we are fetching the data from the database by searching it based on the user id.

    def get_portfolio(self, user_id):
        cursor = self.conn.execute(
            'SELECT symbol, shares, avg_price FROM portfolio WHERE user_id=?',
            (user_id,)
        )
        return cursor.fetchall()
    

    def get_crypto_data(self,user_id):
        cursor = self.conn.execute(
            'SELECT symbol, crypto_amount, avg_price FROM crypto_portfolio WHERE user_id = ?',
            (user_id,)
        )
        return cursor.fetchall()
    
    # to get current email, since email is not stored in user session state.
    def get_current_email(self, user_id):
        cursor = self.conn.execute(
            'SELECT email FROM users WHERE id=?',
            (user_id,)
        )
        return cursor.fetchone()
    

    def change_email(self, user_id, new_email):
            self.conn.execute(
                'UPDATE users SET email = ? WHERE id = ?',
                (new_email, user_id)
            )
            self.conn.commit()
        
    def change_password(self, user_id, new_password):
            self.conn.execute(
                'UPDATE users SET password = ? WHERE id = ?',
                (new_password, user_id)
            )
            self.conn.commit()
            

    def get_password(self, user_id):
        cursor = self.conn.execute(
            'SELECT password FROM users WHERE id = ?',
            (user_id,)  # Need comma to make it a tuple!
        )
        result = cursor.fetchone()
        return result[0] if result else None  # Return actual password string


    # Function to update the portfolio. When a user buys or sells a stock, update_portfolio function is called to change the user's portfolio.
    def update_portfolio(self, user_id, symbol, shares, price, is_buy):
        # Here the is_buy is a boolean. If it's a buy, then is_buy = True else False.
        cursor = self.conn.execute(
            'SELECT shares, avg_price FROM portfolio WHERE user_id = ? AND symbol=?',
            (user_id, symbol)
        )
        existing = cursor.fetchone()
        # We are storing the row into existing named list. 
        # If the user has buyed an existing stock's , then the existing list will contain that stock and the below 
        # if statement will be executed meaning that the stock values will be changed in the user's portfolio 
        # But if it's a complete new stock, then it will not be contained by the existing list, so the else condition will be called and a new stock will be added into the user's portfolio
        
        # Calculate transaction value
        transaction_value = shares * price
        
        try:
            if is_buy:
                if existing:
                    new_shares = existing[0] + shares  # Total new share count
                    old_total_value = existing[0] * existing[1]  # Old shares * Old avg price
                    new_purchase_value = shares * price  # New shares * New price
                    new_avg_price = (old_total_value + new_purchase_value) / new_shares
                    
                    self.conn.execute(
                        'UPDATE portfolio SET shares=?, avg_price=? WHERE user_id=? AND symbol=?',
                        (new_shares, new_avg_price, user_id, symbol)
                    )
                else:
                    self.conn.execute(
                        'INSERT INTO portfolio (user_id, symbol, shares, avg_price) VALUES (?, ?, ?, ?)',
                        (user_id, symbol, shares, price)
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
                            'DELETE FROM portfolio WHERE user_id = ? AND symbol=?',
                            (user_id, symbol)
                        )
                else:
                    # Returning false if the stock is not existing in the database. Since if there's no stock bought, it cannot be sold in the first place
                    return False

            # Update user's balance
            self.conn.execute(
                'UPDATE users SET balance = balance + ? WHERE id=?',
                (-transaction_value if is_buy else transaction_value, user_id)
            )

            # Record the transaction
            self.conn.execute(
                'INSERT INTO transactions (user_id, symbol, transaction_type, shares, price) VALUES (?, ?, ?, ?, ?)',
                (user_id, symbol, 'BUY' if is_buy else 'SELL', shares, price)
            )

            self.conn.commit()
            
            # Get and return new balance
            cursor = self.conn.execute('SELECT balance FROM users WHERE id=?', (user_id,))
            return cursor.fetchone()[0]
            
        except Exception as e:
            self.conn.rollback()
            return False


    def update_crypto_portfolio(self, user_id, symbol, crypto_amount, current_price, is_buy):
        cursor = self.conn.execute(
            'SELECT crypto_amount, avg_price FROM crypto_portfolio WHERE user_id = ? AND symbol=?',
            (user_id, symbol)
        )
        existing = cursor.fetchone()

        # Calculate transaction value
        transaction_value = crypto_amount * current_price

        if is_buy:
            # Here we have to update the average price.
            # Average price -> 100 coin at 1 dollar,  100 coin at 5 dollar. then the average would be -> 3 dollar 200 coin. as 100 + 500.

            # Here's the example for the average price that was implemented in the stock average price.
            # new_shares = existing[0] + shares  # Total new share count
            # old_total_value = existing[0] * existing[1]  # Old shares * Old avg price
            # new_purchase_value = shares * price  # New shares * New price
            # new_avg_price = (old_total_value + new_purchase_value) / new_shares
            if existing:
                new_amount = existing[0] + crypto_amount
                old_total_value = existing[0] * existing[1]  # Old amount * Old avg price
                new_purchase_value = crypto_amount * current_price  # New amount * New price
                new_avg_price = (old_total_value + new_purchase_value) / new_amount
                
                self.conn.execute(
                    'UPDATE crypto_portfolio SET crypto_amount=?, avg_price=? WHERE user_id = ? AND symbol = ?',
                    (new_amount, new_avg_price, user_id, symbol)
                )
            else:
                self.conn.execute(
                    'INSERT INTO crypto_portfolio (user_id, symbol, crypto_amount, avg_price) VALUES (?, ?, ?, ?)',
                    (user_id, symbol, crypto_amount, current_price)
                )
        else:
            if existing and existing[0] >= crypto_amount:
                new_amount = existing[0] - crypto_amount
                if new_amount > 0:
                    self.conn.execute(
                        'UPDATE crypto_portfolio SET crypto_amount=? WHERE user_id=? AND symbol=?',
                        (new_amount, user_id, symbol)
                    )
                else:
                    self.conn.execute(
                        'DELETE FROM crypto_portfolio WHERE user_id = ? AND symbol=?',
                        (user_id, symbol)
                    )
            else:
                return False

        # Update user's balance
        self.conn.execute(
            'UPDATE users SET balance = balance + ? WHERE id=?',
            (-transaction_value if is_buy else transaction_value, user_id)
        )

        # Record the transaction
        self.conn.execute(
            'INSERT INTO transactions (user_id, symbol, transaction_type, shares, price) VALUES (?, ?, ?, ?, ?)',
            (user_id, symbol, 'BUY' if is_buy else 'SELL', crypto_amount, current_price)
        )

        self.conn.commit()
        
        # Get and return new balance
        cursor = self.conn.execute('SELECT balance FROM users WHERE id=?', (user_id,))
        return cursor.fetchone()[0]