import streamlit as st
import requests

# in this file, we are going to use coinbase free api to get all the data for crypto. (Just for practice)
# for coinbase.
api_key = '67a74d22-475c-4e1b-9f01-1803a25181f4'
api_secret = 'MHcCAQEEILp9o7wput6Lplmf+r1OBsCnZ+Zu9I32XAaZdQ+DUmI7oAoGCCqGSM49AwEHoUQDQgAEHJJJJdP8l+sv/rQlsvUf1h09pVpb+xCtuTwLfzuTwsxCFo+6FSknfwpuC0/Scp4se+SZwtXtXC+bWENKihthpA'

# using coingecko.
def load_crypto():
   st.title('Top 10 Cryptocurrencies')
   symbol = st.text_input('Search a crypto-currency', '').upper()
   
   url = "https://api.coingecko.com/api/v3/coins/markets"
   params = {
       'vs_currency': 'usd',
       'order': 'market_cap_desc',
       'per_page': 10,
       'page': 1,
       'sparkline': False
   }
   
   try:
       response = requests.get(url, params=params)
       data = response.json()
       
       for coin in data:
           col1, col2, col3 = st.columns([2,2,2])
           with col1:
               st.write(f"**{coin['name']} ({coin['symbol'].upper()})**")
           with col2:
               st.write(f"${coin['current_price']:,.2f}")
           with col3:
               change = coin['price_change_percentage_24h']
               color = 'green' if change > 0 else 'red'
               st.markdown(f"<span style='color:{color}'>{change:.2f}%</span>", unsafe_allow_html=True)

   except Exception as e:
       st.error("Error fetching cryptocurrency data")
