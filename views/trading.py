import streamlit as st
from models.stock import StockData
from utils.formatters import format_number
from utils.stock_utils import create_stock_chart
from database.connection import get_database
from datetime import datetime


@st.cache_data(ttl="5m")
def fetch_stock_data(symbol):
    """Fetch stock data with caching"""
    return StockData.get_stock_data(symbol)

def create_stock_cards():
    # Popular stock tickers with their names
    popular_stocks = {
        'AAPL': 'Apple',
        'GOOGL': 'Google',
        'MSFT': 'Microsoft',
        'AMZN': 'Amazon',
        'META': 'Meta',
        'TSLA': 'Tesla',
        'NVDA': 'NVIDIA',
        'AMD': 'AMD',
        'NFLX': 'Netflix',
        'DIS': 'Disney'
    }
    
    st.markdown("""
    <style>
        .stock-grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 1rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .stock-card {
            background: linear-gradient(145deg, #1a1f2c, #2a2f3c);
            border: 1px solid #2d3748;
            border-radius: 12px;
            padding: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 0;  /* Added to handle text overflow */
            
        }
        .stock-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            border-color: #805ad5;
        }
        .stock-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        }
        .stock-symbol {
            font-size: 1.1rem;
            font-weight: 700;
            color: #805ad5;
            white-space: nowrap;
        }
        .stock-name {
            color: #a0aec0;
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .stock-price-container {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        .stock-price {
            font-size: 1.2rem;
            font-weight: bold;
            color: #e2e8f0;
            margin-bottom: 0.3rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }
        .price-change {
            padding: 0.2rem 0.8rem;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            white-space: nowrap;
        }
        .positive {
            color: #48bb78;
            background: rgba(72, 187, 120, 0.1);
            border: 1px solid rgba(72, 187, 120, 0.2);
        }
        .negative {
            color: #f56565;
            background: rgba(245, 101, 101, 0.1);
            border: 1px solid rgba(245, 101, 101, 0.2);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="stock-grid-container">', unsafe_allow_html=True)
    
    for symbol, name in popular_stocks.items():
        hist_data, _ = fetch_stock_data(symbol)
        
        if hist_data is not None and not hist_data.empty:
            current_price = hist_data['Close'].iloc[-1]
            prev_price = hist_data['Close'].iloc[-2]
            price_change = ((current_price - prev_price) / prev_price) * 100
            is_positive = price_change >= 0
            
            st.markdown(f"""
                <div class="stock-card" onclick="
                    document.querySelector('input[aria-label*=\'Stock Symbol\']').value = '{symbol}';
                    document.querySelector('input[aria-label*=\'Stock Symbol\']').dispatchEvent(new Event('input', {{ bubbles: true }}));
                ">
                    <div class="stock-header">
                        <div class="stock-symbol">{symbol}</div>
                    </div>
                    <div class="stock-name">{name}</div>
                    <div class="stock-price-container">
                        <div class="stock-price">${current_price:.2f}</div>
                        <div class="price-change {'positive' if is_positive else 'negative'}">
                            {'+' if is_positive else ''}{price_change:.2f}%
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    # Function for loading the trading page
def trading_page():
    st.title('Trading Dashboard')
    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL, GOOGL)', '').upper()
    content_placeholder = st.empty()
    # Stock symbol input

    if not symbol:
        create_stock_cards()
    else:
        content_placeholder.empty()
        hist_data, stock_info = StockData.get_stock_data(symbol)  

        # Add error handling for empty data
        if hist_data is not None and not hist_data.empty and stock_info is not None:
            # Display stock info
            col1, col2, col3 = st.columns(3)
            try:
                current_price = hist_data['Close'].iloc[-1]
                
                # Displaying the stock's values that were fetched from yfinance
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
                                db = get_database()
                                # Calling the update_portfolio function from the database with the argments as the user's id symbol, shares, current_price, and if it's a buy or a sell
                                if db.update_portfolio(st.session_state.user['id'], symbol, shares_to_buy, current_price, True):
                                    st.success(f'Successfully bought {shares_to_buy} shares of {symbol}')
                                    st.session_state.user['balance'] -= total_share_cost  # substracting the amount from the user's total balance
                                    st.rerun()
                                else:
                                    st.error('Transaction Failed. Please try later')  # else Failed
                

                # for selling the stock
                with col2:
                    with st.form('sell_form'):
                        st.subheader('Sell Stock')
                        shares_to_sell = st.number_input('Number of shares to sell', min_value=0.0, step=1.0)
                        total_share_cost_for_selling = shares_to_sell * current_price
                        st.write(f'Total Cost : ${total_share_cost:.2f}')
                        sell_submit_btn = st.form_submit_button('Sell')

                        if sell_submit_btn:

                            db = get_database()
                            
                            # Firstly checking if the user has enough shares to sell. If not then error
                            if db.update_portfolio(st.session_state.user['id'], symbol, shares_to_sell, current_price, False):
                                st.success(f'Successfully Sold {shares_to_sell} shares of {symbol}')  # User had shares for that stocks so sell 
                                st.session_state.user['balance'] += total_share_cost_for_selling
                                st.rerun()
                            else:
                                st.error('Insufficient amount of Shares')  # else failed
            except (IndexError, KeyError) as e:
                    st.error(f"Error loading data for {symbol}. Please try again or check if the symbol is correct.")
        else:
            st.error('Invalid stock symbol or error fetching the data. Please check the symbol and try again.')


    if symbol:
        st.markdown("---")
        st.subheader(f"Latest News for {symbol}")
        
        with st.spinner('Loading news...'):
            news = StockData.get_stock_news(symbol)
            
            if news:
                for item in news:
                    with st.container():
                        col1, col2 = st.columns([7,3])  # 70% for text, 30% for image
                        
                        with col1:
                            # Clean up the title and remove any special text
                            title = item.get('title', '').replace('[Read more]', '').strip()
                            
                            # Clean up the summary - safely handle None values
                            summary = item.get('summary', '')
                            if summary:  # Only process if summary exists
                                summary = summary.replace('In This Article:', '').replace('\n', ' ').strip()
                            else:
                                summary = "No summary available."
                            
                            # Use the published time from the news item instead of current time
                            published_time = item.get('published', datetime.now().strftime('%Y-%m-%d %H:%M'))
                            
                            st.markdown(f"""
                            ### {title}
                            <p style="color: #666; font-size: 0.8em;">{published_time}</p>
                            
                            {summary}
                            
                            <a href="{item.get('link', '#')}" target="_blank" style="color: #3b82f6; text-decoration: none;">Read Article</a>
                            """, unsafe_allow_html=True)
                        
                        if item.get('image'):
                            with col2:
                                st.image(item['image'], use_container_width=True)
                        
                        st.markdown("<hr style='margin: 2rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
            else:
                st.info(f"No recent news available for {symbol}")