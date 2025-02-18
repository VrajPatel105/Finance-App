# Importing required libraries
import streamlit as st
import yfinance as yf
import streamlit.components.v1 as components

# Here we are embedding a TradingView chart widget into a web page. This is provided from tradingview officially for it to use by developers.

# chart for stock
def create_stock_chart(symbol):
    st.markdown("""
    <style>
    body {
        background-color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

        # here we are 
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


# chart for crypto..
def create_crypto_chart(symbol):
    st.markdown("""
    <style>
    body {
        background-color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

    # TradingView Chart Embedded using st.components.html()
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
                    "symbol": "BINANCE:{symbol}USDT",
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
