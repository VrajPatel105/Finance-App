import streamlit as st
from models.stock import StockData
from utils.formatters import format_number
from utils.stock_utils import create_stock_chart
from database.db_manager import Database
from datetime import datetime

# Function for loading the trading page
def trading_page():
    st.title('Trading Dashboard')
    
    # Stock symbol input
    symbol = st.text_input('Enter Stock Symbol (e.g., AAPL, GOOGL)', '').upper()

    if symbol:
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
                                db = Database()
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

                            db = Database()
                            
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