import streamlit as st
import requests
from models.crypto_data import load_crypto_details

# in this file, we are going to use coinbase free api to get all the data for crypto. (Just for practice)
# for coinbase.
# api_key = '67a74d22-475c-4e1b-9f01-1803a25181f4'
# api_secret = 'MHcCAQEEILp9o7wput6Lplmf+r1OBsCnZ+Zu9I32XAaZdQ+DUmI7oAoGCCqGSM49AwEHoUQDQgAEHJJJJdP8l+sv/rQlsvUf1h09pVpb+xCtuTwLfzuTwsxCFo+6FSknfwpuC0/Scp4se+SZwtXtXC+bWENKihthpA'

import streamlit as st
import requests

def load_crypto():
    st.title('Cryptocurrencies')
    user_input = st.text_input('Search a crypto-currency', '').upper()

    if user_input:
        load_crypto_details(user_input)
    

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': False
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Create 3x4 grid for cards
        cols = st.columns(3)
        
        for idx, coin in enumerate(data):
            col_idx = idx % 3
            with cols[col_idx]:
                with st.container():
                    st.markdown(
                        f"""
                        <div style='
                            padding: 1rem;
                            border-radius: 0.5rem;
                            background-color: #1E293B ;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            margin-bottom: 1rem;
                        '>
                            <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                                <img src='{coin["image"]}' style='width: 80px; height: 80px; margin-right: 0.5rem;'>
                                <strong>{coin["name"]} ({coin["symbol"].upper()})</strong>
                            </div>
                            <div style='font-size: 1.25rem; margin-bottom: 0.5rem;'>
                                ${coin["current_price"]:,.5f}
                            </div>
                            <div style='color: {"#4ee048" if coin["price_change_percentage_24h"] > 0 else "red"}'>
                                {coin["price_change_percentage_24h"]:.2f}%
                            </div>
                            <div style='font-size: 0.875rem; color: #F87171 ;'>
                                Market Cap: ${coin["market_cap"]:,.0f}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    except Exception as e:
        st.error("Error fetching cryptocurrency data")
