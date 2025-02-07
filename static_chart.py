import streamlit as st
import yfinance as yf
import streamlit.components.v1 as components

# Set Streamlit Page Config
st.set_page_config(page_title="TradingView Stock Chart", page_icon="📈", layout="wide")

# Sidebar for Stock Symbol
st.sidebar.header("TradingView Chart Settings")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL").upper()

# Fetch stock data for validation
def validate_stock(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="1d")  # Fetch latest data
        if df.empty:
            return False
        return True
    except Exception:
        return False

# Validate Symbol
if validate_stock(symbol):

    # TradingView Chart Embed using st.components.html()
    tradingview_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        </head>
        <body>
            <div class="tradingview-widget-container">
                <div id="tradingview_chart"></div>
                <script type="text/javascript">
                new TradingView.widget(
                {{
                    "width": "100%",
                    "height": 600,
                    "symbol": "NASDAQ:{symbol}",
                    "interval": "D",
                    "timezone": "Etc/UTC",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "toolbar_bg": "#131722",
                    "enable_publishing": false,
                    "allow_symbol_change": true,
                    "container_id": "tradingview_chart"
                }});
                </script>
            </div>
        </body>
        </html>
    """

    # Display TradingView chart in Streamlit
    components.html(tradingview_html, height=650)

else:
    st.error(f"❌ Invalid Stock Symbol: '{symbol}'. Please enter a valid stock symbol.")




# for crypto tradingview_symbol = f"BINANCE:{symbol_input}USDT"
