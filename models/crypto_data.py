import streamlit as st
import requests
from datetime import datetime
from database.connection import get_database
import streamlit as st
from streamlit.components.v1 import html
import time
from streamlit_lottie import st_lottie
from utils.stock_utils import create_crypto_chart
import json
from utils.formatters import format_number

def load_crypto_details(user_input):
   

    def load_transaction_complete_lottie(flag):

        if flag:
            def load_lottieurl(url: str):
                    r = requests.get(url)
                    r.raise_for_status()
                    return r.json()

            transaction_complete_lottie = "https://lottie.host/1c4c35ec-5ff0-4485-a777-8ed0f60b16e7/1mDPJ8vsSy.json"

            
            st.markdown('<div class="lottie-overlay"></div>', unsafe_allow_html=True)
            lottie_json = load_lottieurl(transaction_complete_lottie)

            st.markdown("""
            <style>
            .lottie-overlay {
                position: fixed;
                top:: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
            }
            </style>
            """, unsafe_allow_html=True)

            if lottie_json:
                st_lottie(
                    lottie_json,
                    speed=1,
                    loop=True,
                    height=300,
                    width=300,
                    key="lottie"
                )
                time.sleep(1) 
                flag = False

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

    st.subheader(f"{user_input}")
    
    if user_input:
        cmc_api_key = st.secrets['X-CMC_PRO_API_KEY']
        headers = {
            'X-CMC_PRO_API_KEY': cmc_api_key,
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
                        st.image(img_data['image']['large'], width=150)
                    except:
                        st.warning("Unable to load coin image")

                with col2:
                    change_24h = price_data['percent_change_24h']
                    st.components.v1.html(f"""
                        <div style='
                            background: #1F1F1F;
                            border: 1px solid rgba(168, 85, 247, 0.2);
                            border-radius: 10px;
                            padding: 1.2rem;
                            box-shadow: 0 0 15px rgba(168, 85, 247, 0.1);
                        '>
                            <h2 style='
                                font-size: 1.6rem;
                                font-weight: 700;
                                margin: 0 0 0.9rem 0;
                                background: linear-gradient(to right, #E2E8F0, #A855F7);
                                -webkit-background-clip: text;
                                -webkit-text-fill-color: transparent;
                                line-height: 1;
                            '>{coin_data['name']}
                                <span style='
                                    font-size: 1.1rem;
                                    color: #A855F7;
                                    background: none;
                                    padding-bottom: 20px;
                                    -webkit-text-fill-color: #A855F7;
                                '>({coin_data['symbol']})</span>
                            </h2>
                            
                            <h3 style='
                                font-size: 2rem;
                                font-weight: 400;
                                margin: 0.3rem 0;
                                color: #E2E8F0;
                                line-height: 1;
                            '>${price_data['price']:,.2f}
                                <span style='
                                    font-size: 1rem;
                                    color: #94A3B8;
                                '>USD</span>
                            </h3>
                            
                            <p style='
                                font-size: 1.1rem;
                                font-weight: 500;
                                color: {"#4ADE80" if change_24h > 0 else "#FB7185"};
                                margin: 0;
                                padding-top: 12px;

                                line-height: 1;
                            '>{change_24h:+.2f}%
                                <span style='
                                    font-size: 0.85rem;
                                    color: #94A3B8;
                                '>(24h)</span>
                            </p>
                        </div>
                    """, height=200)
                # calling the chart function.
                create_crypto_chart(user_input)


                col1, col2 = st.columns(2)

                with col1:
                    with st.form(key='buy_crypto'):
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
                                    db = get_database()
                                    new_balance = db.update_crypto_portfolio(st.session_state.user['id'], user_input, crypto_amount, price_data['price'], True)
                                    if new_balance is not False:
                                        st.session_state.user['balance'] = new_balance
                                        st.success('Purchase successful!')
                                        
                                        # Update query parameters
                                        state_data = {
                                            'logged_in': st.session_state.logged_in,
                                            'current_page': st.session_state.current_page,
                                            'user': st.session_state.user
                                        }
                                        st.query_params['session_state'] = json.dumps(state_data)
                                        
                                        load_transaction_complete_lottie(True)
                                        st.rerun()
                                    else:
                                        st.error('Transaction failed. Please try again.')
                            else:
                                st.error('User balance information unavailable.')

                with col2:
                    with st.form(key='sell_crypto'):
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
                                db = get_database()
                                new_balance = db.update_crypto_portfolio(st.session_state.user['id'], user_input, sell_amount, price_data['price'], False)
                                if new_balance is not False:
                                    st.session_state.user['balance'] = new_balance
                                    st.success('Sold successfully!')
                                    
                                    # Update query parameters
                                    state_data = {
                                        'logged_in': st.session_state.logged_in,
                                        'current_page': st.session_state.current_page,
                                        'user': st.session_state.user
                                    }
                                    st.query_params['session_state'] = json.dumps(state_data)
                                    
                                    load_transaction_complete_lottie(True)
                                    st.rerun()
                                else:
                                    st.error('Insufficient crypto balance!')
                            else:
                                st.error('User balance information unavailable.')

                # Market Metrics
                st.subheader("Market Metrics")
                col1, col2, col3 = st.columns(3)
                metrics = {
                    "Market Cap": format_number(float(price_data['market_cap'])),
                    "24h Volume": format_number(float(price_data['volume_24h'])),
                    "Circulating Supply": format_number(float(coin_data['circulating_supply']))
                }

                # Display each metric in its column
                col1.markdown(f"""
                    <div class="crypto-card">
                        <p class="metric-label">Market Cap</p>
                        <p class="metric-value">{metrics['Market Cap']}</p>
                    </div>
                """, unsafe_allow_html=True)

                col2.markdown(f"""
                    <div class="crypto-card">
                        <p class="metric-label">24h Volume</p>
                        <p class="metric-value">{metrics['24h Volume']}</p>
                    </div>
                """, unsafe_allow_html=True)

                col3.markdown(f"""
                    <div class="crypto-card">
                        <p class="metric-label">Circulating Supply</p>
                        <p class="metric-value">{metrics['Circulating Supply']}</p>
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