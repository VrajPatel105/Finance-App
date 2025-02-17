import streamlit as st
import requests
from models.crypto_data import load_crypto_details

# Using coin gecko api to fetch data about crypto.

def load_crypto():
    st.title('Cryptocurrencies')
    # getting input from the user
    st.markdown("""
        <style>
        img {
            loading: lazy;
        }
        </style>
    """, unsafe_allow_html=True)
    user_input = st.text_input('Search a crypto-currency', '').upper()

    if user_input:
        # loading the crypto details based on the user's input entered.
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
        
        # Creating 3x4 grid for cards
        cols = st.columns(3)
        
        for idx, coin in enumerate(data):
            col_idx = idx % 3
            with cols[col_idx]:
                with st.container():
                    st.markdown(
                        f"""
                        <div style='
                            padding: 1.5rem;
                            border-radius: 12px;
                            background-color: #1F1F1F;
                            border: 1px solid rgba(168, 85, 247, 0.2);
                            box-shadow: 0 0 15px rgba(168, 85, 247, 0.1);
                            margin-bottom: 1.2rem;
                            transition: all 0.3s ease;
                            &:hover {{
                                border-color: rgba(168, 85, 247, 0.4);
                                box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
                                transform: translateY(-2px);
                            }}
                        '>
                            <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                                <img src='{coin["image"]}' style='width: 60px; height: 60px; margin-right: 1rem; border-radius: 50%;'>
                                <div>
                                    <div style='font-size: 1.2rem; font-weight: 600; color: #E2E8F0; margin-bottom: 0.3rem;'>
                                        {coin["name"]}
                                    </div>
                                    <div style='color: #A855F7; font-size: 0.9rem;'>
                                        {coin["symbol"].upper()}
                                    </div>
                                </div>
                            </div>
                            <div style='
                                font-size: 1.8rem;
                                font-weight: 700;
                                margin: 0.8rem 0;
                                background: linear-gradient(to right, #E2E8F0, #A855F7);
                                -webkit-background-clip: text;
                                -webkit-text-fill-color: transparent;
                            '>
                                ${coin["current_price"]:,.5f}
                            </div>
                            <div style='
                                font-size: 1.1rem;
                                color: {"#4ADE80" if coin["price_change_percentage_24h"] > 0 else "#FB7185"};
                                margin: 0.5rem 0;
                                font-weight: 500;
                            '>
                                {coin["price_change_percentage_24h"]:.2f}%
                            </div>
                            <div style='
                                font-size: 0.9rem;
                                color: #94A3B8;
                                margin-top: 0.5rem;
                            '>
                                Market Cap: ${coin["market_cap"]:,.0f}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    except Exception as e:
        st.error("Error fetching cryptocurrency data")
