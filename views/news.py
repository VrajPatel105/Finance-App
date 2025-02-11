# Import required libraries for building our finance news dashboard
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import time
import os

# API keys are stored securely in Streamlit's secrets management
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
ALPHA_VANTAGE_API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]

def fetch_stock_news():
    """Fetch real-time stock market news from NewsAPI - returns top 10 most recent articles
    about stocks, markets, NYSE, or NASDAQ in English"""
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWS_API_KEY,
            "q": "(stock OR market OR NYSE OR NASDAQ)",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        return [{
            "title": article["title"],
            "description": article["description"],
            "source": article["source"]["name"],
            "date": datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
            "url": article["url"]
        } for article in articles if article["description"]]
    except Exception as e:
        st.error(f"Error fetching stock news: {str(e)}")
        return []

def fetch_crypto_news():
    """Fetch real-time cryptocurrency news from CryptoCompare - returns latest 10 articles
    with truncated descriptions for better readability"""
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/"
        params = {
            "api_key": ALPHA_VANTAGE_API_KEY,
            "sortOrder": "latest"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("Data", [])[:10]
        
        return [{
            "title": article["title"],
            "description": article["body"][:200] + "...",
            "source": article["source"],
            "date": datetime.fromtimestamp(article["published_on"]),
            "url": article["url"]
        } for article in articles]
    except Exception as e:
        st.error(f"Error fetching crypto news: {str(e)}")
        return []

def fetch_market_data():
    """Fetch real-time market data for S&P 500, Bitcoin, and Ethereum from Alpha Vantage.
    Returns current prices and price changes where available."""
    try:
        # Fetch S&P 500 data using SPY ETF as proxy
        sp500_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SPY&apikey={ALPHA_VANTAGE_API_KEY}"
        sp500_response = requests.get(sp500_url)
        sp500_data = sp500_response.json().get("Global Quote", {})
        
        # Get current Bitcoin/USD exchange rate
        btc_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={ALPHA_VANTAGE_API_KEY}"
        btc_response = requests.get(btc_url)
        btc_data = btc_response.json().get("Realtime Currency Exchange Rate", {})
        
        # Get current Ethereum/USD exchange rate
        eth_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=ETH&to_currency=USD&apikey={ALPHA_VANTAGE_API_KEY}"
        eth_response = requests.get(eth_url)
        eth_data = eth_response.json().get("Realtime Currency Exchange Rate", {})
        
        return {
            "sp500": {
                "price": float(sp500_data.get("05. price", 0)),
                "change": float(sp500_data.get("09. change", 0)),
                "change_percent": float(sp500_data.get("10. change percent", "0").strip("%"))
            },
            "btc": {
                "price": float(btc_data.get("5. Exchange Rate", 0)),
                "change_percent": 0  # Alpha Vantage doesn't provide change % for crypto
            },
            "eth": {
                "price": float(eth_data.get("5. Exchange Rate", 0)),
                "change_percent": 0
            }
        }
    except Exception as e:
        st.error(f"Error fetching market data: {str(e)}")
        return None
    
def load_news():
    st.markdown("""
    <style>
        /* Make links look clean and modern by removing default underlines */
        div[data-testid="stAppViewContainer"] a {
            text-decoration: none !important;
        }

        div[data-testid="stAppViewContainer"] a:hover {
            text-decoration: none !important;
        }

        .news-card-link {
            text-decoration: none !important;
            color: inherit !important;
        }

        .news-card-link:hover {
            text-decoration: none !important;
        }
                    
        /* News card styling with modern glass-morphism effect */
        div.news-card {
            /* Dark gradient background for depth */
            background: linear-gradient(145deg, #0a0a0a 0%, #111111 100%);
            padding: 1.75rem;
            /* Rounded corners for modern look */
            border-radius: 20px;
            margin: 1.25rem 0;
            /* Subtle purple border with low opacity */
            border: 1px solid rgba(147, 51, 234, 0.1);
            /* Soft shadow for depth */
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            /* Smooth transition for hover effects */
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        /* Hover effects for news cards */
        div.news-card:hover {
            /* Slight lift effect */
            transform: translateY(-6px);
            /* Enhanced purple glow */
            box-shadow: 0 8px 30px rgba(147, 51, 234, 0.2);
            border-color: rgba(147, 51, 234, 0.3);
            /* Slightly darker gradient on hover */
            background: linear-gradient(145deg, #0d0d0d 0%, #141414 100%);
        }
        
        /* Purple accent line on the left side of cards */
        div.news-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 5px;
            /* Purple gradient for visual interest */
            background: linear-gradient(180deg, #9333EA 0%, #A855F7 100%);
            border-radius: 4px 0 0 4px;
            opacity: 0.8;
            transition: width 0.3s ease;
        }
        
        /* Thicken the purple line on hover */
        div.news-card:hover::before {
            width: 7px;
        }
        
        /* News card title styling */
        div.news-card h3 {
            color: #ffffff;
            margin-bottom: 1.25rem;
            font-size: 1.35rem;
            font-weight: 600;
            line-height: 1.4;
            padding-left: 0.5rem;
        }
        
        /* News description text styling */
        div.news-card p {
            color: #94a3b8;
            line-height: 1.7;
            font-size: 1rem;
            padding-left: 0.5rem;
            margin-bottom: 1.5rem;
        }
        
        /* Source tag styling with glass effect */
        .source-tag {
            /* Semi-transparent purple background */
            background: rgba(147, 51, 234, 0.15);
            color: #A855F7;
            padding: 8px 16px;
            border-radius: 30px;
            font-size: 0.9em;
            font-weight: 500;
            letter-spacing: 0.3px;
            /* Subtle border for depth */
            border: 1px solid rgba(147, 51, 234, 0.2);
            backdrop-filter: blur(8px);
        }
        
        /* Container for source and date */
        .news-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 0.5rem;
        }
        
        /* Date display styling */
        .news-date {
            color: #718096;
            font-size: 0.9em;
            font-weight: 400;
            letter-spacing: 0.5px;
        }
        
        /* Refresh button styling */
        section.main .stButton > button {
            background-color: #9333EA;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 500;
            box-shadow: 0 0 15px rgba(147, 51, 234, 0.2);
            transition: all 0.3s ease;
        }
        
        /* Hover effect for refresh button */
        section.main .stButton > button:hover {
            background-color: #A855F7;
            transform: translateY(-2px);
        }
        
        /* Tab navigation styling */
        section.main .stTabs [data-baseweb="tab-list"] {
            /* Semi-transparent dark background */
            background: rgba(10, 10, 10, 0.8);
            padding: 0.5rem;
            border-radius: 12px;
            border: 1px solid rgba(147, 51, 234, 0.2);
        }
        
        /* Individual tab styling */
        section.main .stTabs [data-baseweb="tab"] {
            color: #e6e9ef;
            border-radius: 8px;
            padding: 12px 24px;
            margin: 0 4px;
        }
        
        /* Active tab highlighting */
        section.main .stTabs [aria-selected="true"] {
            background: #9333EA !important;
        }
        
        /* Last updated time display */
        section.main .time-display {
            background: #0a0a0a;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.9em;
            color: #A855F7;
            border: 1px solid rgba(147, 51, 234, 0.2);
        }
    </style>
""", unsafe_allow_html=True)
    
    # Main title for the dashboard
    st.title("📈 Finch News Hub")

    # Initialize refresh timestamp in session state
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()

    # Create header with refresh controls
    col1, col2 = st.columns([2, 1])
    with col2:
        # Display last update time
        st.markdown(f'<div class="time-display">Last updated: {st.session_state.last_refresh.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.session_state.last_refresh = datetime.now()
            st.rerun()

    # Create tabs for different news categories
    tabs = st.tabs(["📊 Stocks", "💎 Crypto"])

    # Stock News Tab Content
    with tabs[0]:
        st.header("Stock Market News")
        news_items = fetch_stock_news()
        
        # Display each stock news article in a card
        for news in news_items:
            with st.container():
                st.markdown(f"""
                    <a href="{news['url']}" target="_blank" class="news-card-link" style="text-decoration: none !important;">
                        <div class="news-card">
                            <h3>{news['title']}</h3>
                            <p>{news['description']}</p>
                            <div class="news-meta">
                                <span class="source-tag">{news['source']}</span>
                                <span class="news-date">
                                    {news['date'].strftime('%Y-%m-%d %H:%M')}
                                </span>
                            </div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)

    # Crypto News Tab Content
    with tabs[1]:
        st.header("Cryptocurrency News")
        crypto_news = fetch_crypto_news()
        
        # Display each crypto news article in a card
        for news in crypto_news:
            with st.container():
                st.markdown(f"""
                    <a href="{news['url']}" target="_blank" class="news-card-link" style="text-decoration: none !important;">
                        <div class="news-card">
                            <h3>{news['title']}</h3>
                            <p>{news['description']}</p>
                            <div class="news-meta">
                                <span class="source-tag">{news['source']}</span>
                                <span class="news-date">
                                    {news['date'].strftime('%Y-%m-%d %H:%M')}
                                </span>
                            </div>
                        </div>
                    </a>
                """, unsafe_allow_html=True)