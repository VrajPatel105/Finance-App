import streamlit as st
import requests
from datetime import datetime
from database.db_manager import Database

def load_crypto_details(user_input):
   st.markdown("""
       <style>
       .stApp {background-color: #0E1117}
       .crypto-card {
           background-color: #1E293B;
           padding: 1.5rem;
           border-radius: 0.75rem;
           color: white;
       }
       .metric-value {color: #FFFFFF}
       .metric-label {color: #94A3B8}
       .positive-change {color: #4ADE80}
       .negative-change {color: #F87171}
       </style>
   """, unsafe_allow_html=True)

   st.title(f"{user_input}")
   
   if user_input:
       headers = {
           'X-CMC_PRO_API_KEY': '440c12ff-74f9-4ff9-92a1-07345791e1cb',
           'Accept': 'application/json'
       }
       
       try:
           response = requests.get(
               'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
               headers=headers,
               params={'symbol': user_input}
           )
           data = response.json()
           
           if response.status_code == 200 and user_input in data['data']:
               coin_data = data['data'][user_input]
               price_data = coin_data['quote']['USD']

               # Main Display
               col1, col2 = st.columns([1, 2])
               with col1:
                   try:
                       img_response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_data['slug']}")
                       img_data = img_response.json()
                       st.image(img_data['image']['large'], width=250)
                   except:
                       st.warning("Unable to load coin image")

               with col2:
                   change_24h = price_data['percent_change_24h']
                   st.markdown(f"""
                       <div class="crypto-card">
                           <h2 style='font-size:2rem; margin-bottom:1rem'>{coin_data['name']} ({coin_data['symbol']})</h2>
                           <h3 style='font-size:1.8rem; margin-bottom:0.5rem'>${price_data['price']:,.2f} USD</h3>
                           <p style='font-size:1.2rem; color: {"#4ADE80" if change_24h > 0 else "#F87171"}'>{change_24h:+.2f}% (24h)</p>
                       </div>
                   """, unsafe_allow_html=True)


                # Here add buy and sell button same as did in stocks.

                # Crypto buy / sell form
               col1, col2 = st.columns(2)

               with col1:
                    with st.form(key='buy_crypto', enter_to_submit=True):
                        st.subheader(f'Buy {user_input}')
                        
                        crypto_amount = st.number_input('Amount', min_value=0.1, step=0.1)
                        if 'price' in price_data:
                            crypto_cost = price_data['price'] * crypto_amount
                            st.write(f'Total Cost: ${crypto_cost:.2f}')
                        else:
                            st.error('Price data is unavailable.')
                            crypto_cost = 0

                        crypto_buy_submit_btn = st.form_submit_button('Buy')

                        if crypto_buy_submit_btn:
                            if 'user' in st.session_state and 'balance' in st.session_state.user:
                                if crypto_cost > st.session_state.user['balance']:
                                    st.error('Insufficient funds!')
                                else:
                                    db = Database()
                                    # Assuming a method to handle transaction
                                    if db.update_crypto_portfolio(st.session_state.user['id'],user_input, crypto_amount, crypto_cost, True):
                                        st.success('Purchase successful!')
                                        st.session_state.user['balance'] -= crypto_cost  # substracting the amount from the user's total balance
                                        st.rerun()
                            else:
                                st.error('User balance information unavailable.')

               with col2:
                    with st.form(key='sell_crypto', enter_to_submit=True):
                        st.subheader(f'Sell {user_input}')
                        
                        sell_amount = st.number_input('Amount', min_value=0.1, step=0.1, key='sell_amount')
                        if 'price' in price_data:
                            sell_value = price_data['price'] * sell_amount
                            st.write(f'Total Value: ${sell_value:.2f}')
                        else:
                            st.error('Price data is unavailable.')
                            sell_value = 0
                        
                        sell_submit_btn = st.form_submit_button('Sell')
                        
                        if sell_submit_btn:
                            if 'user' in st.session_state and 'balance' in st.session_state.user:
                                db = Database()
                                if db.update_crypto_portfolio(st.session_state.user['id'], user_input, sell_amount, sell_value, False):
                                    st.success('Sold successfully!')
                                    st.session_state.user['balance'] += crypto_cost
                                    st.rerun()
                                else:
                                    st.error('Insufficient crypto balance!')
                            else:
                                st.error('User balance information unavailable.')

               # Market Metrics
               st.subheader("Market Metrics")
               cols = st.columns(3)
               metrics = {
                   "Market Cap": price_data['market_cap'],
                   "24h Volume": price_data['volume_24h'],
                   "Circulating Supply": coin_data['circulating_supply']
               }
               
               for col, (label, value) in zip(cols, metrics.items()):
                   col.markdown(f"""
                       <div class="crypto-card">
                           <p class="metric-label">{label}</p>
                           <p class="metric-value">${value:,.0f}</p>
                       </div>
                   """, unsafe_allow_html=True)

               # Price Changes
               st.subheader("Price Changes")
               cols = st.columns(3)
               for col, period in zip(cols, ["1h", "24h", "7d"]):
                   change = price_data[f'percent_change_{period}']
                   col.markdown(f"""
                       <div class="crypto-card">
                           <p class="metric-label">{period} Change</p>
                           <p class="{'positive-change' if change > 0 else 'negative-change'}">{change:+.2f}%</p>
                       </div>
                   """, unsafe_allow_html=True)

           else:
               st.error(f"Could not find data for {user_input}")
               
       except Exception as e:
           st.error(f"Error fetching data: {str(e)}")

   st.caption(f"Data provided by CoinMarketCap API | Last updated: {datetime.now().strftime('%B %d, %Y, %I:%M %p')} EST")