import streamlit as st
import streamlit.components.v1 as components

def create_stock_chart(symbol):
    # Set dark background for the stock chart
    st.markdown("""
    <style>
    body {
        background-color: #000000;
    }
    .tradingview-widget-container {
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

def create_crypto_chart(symbol):
    # Set dark background for the crypto chart
    st.markdown("""
    <style>
    body {
        background-color: #000000;
    }
    .tradingview-widget-container {
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