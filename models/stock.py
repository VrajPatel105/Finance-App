import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
import random

class StockData:
    # Function to get the live data from the the market using yfinance api
    @staticmethod
    def get_stock_data(symbol, period='1y'):
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period)
            info = stock.info
            return hist, info  # This will return history of the stock. hist will be a "DataFrame". Info will be a dictionary
        except:
            return None, None

    @staticmethod
    def get_portfolio_history(db, user_id, time_period='1y'):
        """
        Calculate historical portfolio value based on transactions with time period filtering
        
        Parameters:
        - db: Database instance
        - user_id: User ID
        - time_period: String ('3d', '5d', '1m', '6m', '1y')
        
        Returns: DataFrame with timestamps and portfolio values
        """
        # Calculate the start date based on the time period
        current_date = datetime.now()
        if time_period == '3d':
            start_date = current_date - timedelta(days=3)
        elif time_period == '5d':
            start_date = current_date - timedelta(days=5)
        elif time_period == '1m':
            start_date = current_date - timedelta(days=30)
        elif time_period == '6m':
            start_date = current_date - timedelta(days=180)
        else:  # 1y default
            start_date = current_date - timedelta(days=365)
        
        # Get all transactions up to the current date
        cursor = db.conn.execute(
            '''
            SELECT symbol, transaction_type, shares, price, timestamp 
            FROM transactions 
            WHERE user_id = ? 
            ORDER BY timestamp
            ''', 
            (user_id,)
        )
        transactions = cursor.fetchall()
        
        # Initialize tracking variables
        portfolio_values = []
        current_holdings = {}
        invested_amount = 0
        
        # Process all transactions to get the initial state
        initial_transactions = [t for t in transactions if datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S') < start_date]
        
        # Calculate initial state from older transactions
        for trans in initial_transactions:
            symbol, trans_type, shares, price, _ = trans
            if trans_type == 'BUY':
                invested_amount += shares * price
                if symbol not in current_holdings:
                    current_holdings[symbol] = 0
                current_holdings[symbol] += shares
            else:  # SELL
                invested_amount -= shares * price
                current_holdings[symbol] -= shares
        
        # Process transactions within the selected time period
        relevant_transactions = [t for t in transactions if datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S') >= start_date]
        
        # If no transactions in period, add current state at start date
        if not relevant_transactions and current_holdings:
            total_value = 0
            for sym, share_count in current_holdings.items():
                if share_count > 0:
                    hist_data, _ = StockData.get_stock_data(sym, period='1d')
                    if hist_data is not None and not hist_data.empty:
                        current_price = hist_data['Close'].iloc[-1]
                        total_value += share_count * current_price
            
            portfolio_values.append({
                'timestamp': start_date,
                'invested': invested_amount,
                'market_value': total_value,
                'profit_loss': total_value - invested_amount
            })
        
        # Process transactions within the time period
        for trans in relevant_transactions:
            symbol, trans_type, shares, price, timestamp = trans
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            
            if trans_type == 'BUY':
                invested_amount += shares * price
                if symbol not in current_holdings:
                    current_holdings[symbol] = 0
                current_holdings[symbol] += shares
            else:  # SELL
                invested_amount -= shares * price
                current_holdings[symbol] -= shares
            
            total_value = 0
            for sym, share_count in current_holdings.items():
                if share_count > 0:
                    hist_data, _ = StockData.get_stock_data(sym, period='1d')
                    if hist_data is not None and not hist_data.empty:
                        current_price = hist_data['Close'].iloc[-1]
                        total_value += share_count * current_price
            
            portfolio_values.append({
                'timestamp': dt,
                'invested': invested_amount,
                'market_value': total_value,
                'profit_loss': total_value - invested_amount
            })
        
        return pd.DataFrame(portfolio_values)




    @staticmethod
    def get_stock_news(symbol):
        try:
            API_KEY = "e92fe2a711264deea18ed1db329d7e15"
            url = f"https://newsapi.org/v2/everything?q={symbol}+stock&apiKey={API_KEY}&language=en&sortBy=publishedAt"
            
            response = requests.get(url)
            data = response.json()
            
            if data.get('articles'):
                formatted_news = []
                for item in data['articles'][:5]:
                    news_item = {
                        'title': item.get('title', 'No Title Available'),
                        'publisher': item.get('source', {}).get('name', 'Unknown Publisher'),
                        'link': item.get('url', '#'),
                        'published': item.get('publishedAt', '').replace('T', ' ').replace('Z', ''),
                        'summary': item.get('description', ''),
                        'image': item.get('urlToImage')
                    }
                    formatted_news.append(news_item)
                return formatted_news
            return None
        except Exception as e:
            print(f"Error in fetching news : {e}")
            return None
            