import streamlit as st
import requests
from datetime import datetime

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