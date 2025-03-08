# Finch Trading Platform

A modern, AI-powered stock and cryptocurrency trading platform built with Streamlit and Python. Finch offers real-time market data, portfolio management, AI-assisted trading insights, and secure user authentication.

## Features

### Trading & Portfolio Management
- Real-time stock and cryptocurrency trading
- Portfolio tracking and analysis
- Interactive charts using TradingView integration
- Transaction history and performance metrics 
- AI-powered trading assistant for market insights 

### Market Data & Analysis
- Real-time stock prices and market data via yfinance
- Cryptocurrency data through CoinMarketCap API
- Advanced technical analysis tools
- News integration through NewsAPI
- Comprehensive market metrics and indicators

### Security & User Management
- Secure user authentication with SHA256 encryption
- Location-based login tracking
- Multi-device session management
- Balance verification and transaction security
- Protected API key management through Streamlit secrets

### User Experience
- Modern, responsive dark theme UI
- Real-time portfolio updates
- Interactive stock cards and crypto listings
- Embedded Spotify player for ambient trading
- AI chatbot for trading assistance

## Tech Stack

- **Frontend**: Streamlit, HTML, CSS
- **Backend**: Python, SQLite
- **Database**: SQLite3
- **APIs**:
  - yfinance (Stock data)
  - CoinMarketCap (Crypto data)
  - NewsAPI (Financial news)
  - IP-API (Location tracking)
  - OpenAI (AI assistant)
  - Spotify (Music integration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finch-trading.git
cd finch-trading
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in `.streamlit/secrets.toml`:
```toml
[api_keys]
X-CMC_PRO_API_KEY = "your_coinmarketcap_api_key"
NEWS_API_KEY = "your_news_api_key"
OPENAI_API_KEY = "your_openai_api_key"
ALPHA_VANTAGE_API_KEY = "your_alphavantage_api_key"
```

4. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
finch-trading/
├── app.py                 # Main application file
├── database/             # Database management
│   ├── connection.py     # Database connection
│   └── db_manager.py     # Database operations
├── models/               # Data models
│   ├── stock.py         # Stock data handling
│   └── crypto_data.py   # Cryptocurrency data handling
├── utils/               # Utility functions
│   ├── formatters.py    # Data formatting
│   └── stock_utils.py   # Stock-related utilities
├── views/               # UI components
│   ├── trading.py       # Trading interface
│   ├── portfolio.py     # Portfolio management
│   ├── crypto.py        # Cryptocurrency interface
│   ├── news.py         # News feed
│   └── ai_assistant.py  # AI trading assistant
└── resources/           # Static resources
```

## API Usage

The platform integrates multiple APIs for comprehensive market data:

- **yfinance**: Real-time stock market data
- **CoinMarketCap**: Cryptocurrency pricing and metrics
- **NewsAPI**: Financial news and market updates
- **OpenAI**: AI-powered trading insights
- **IP-API**: User location tracking

## Security Features

- Password hashing using SHA256
- Session state management
- Location-based login tracking
- API key protection using Streamlit secrets
- Regular balance verification and syncing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- TradingView for chart widgets
- Streamlit for the web framework
- All API providers for their services
