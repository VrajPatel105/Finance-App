import streamlit as st
import plotly.graph_objects as go
from models.stock import StockData
import requests
from database.connection import get_database

# Cache portfolio data fetching
@st.cache_data(ttl="5m")  # Cache for 5 minutes
def fetch_portfolio_data(_db, user_id):
    return _db.get_portfolio(user_id)

@st.cache_data(ttl="5m")
def fetch_crypto_data(_db, user_id):
    return _db.get_crypto_data(user_id)

# Batch fetch stock prices
@st.cache_data(ttl="5m")
def fetch_current_prices(symbols):
    """Batch fetch stock prices for multiple symbols"""
    all_data = {}
    for symbol in symbols:
        hist_data, _ = StockData.get_stock_data(symbol, period='1d')
        if hist_data is not None and not hist_data.empty:
            all_data[symbol] = hist_data['Close'].iloc[-1]
    return all_data

# Batch fetch crypto prices
@st.cache_data(ttl="5m")
def fetch_crypto_prices(symbols):
    """Batch fetch crypto prices"""
    headers = {
        'X-CMC_PRO_API_KEY': '440c12ff-74f9-4ff9-92a1-07345791e1cb',
        'Accept': 'application/json'
    }
    
    # Join all symbols for a single API call
    symbol_string = ','.join(symbols)
    response = requests.get(
        'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
        headers=headers,
        params={'symbol': symbol_string}
    )
    data = response.json()
    
    prices = {}
    for symbol in symbols:
        if symbol in data['data']:
            prices[symbol] = data['data'][symbol]['quote']['USD']['price']
    return prices

@st.cache_data(ttl="5m")
def fetch_portfolio_history(_db, user_id, time_period):
    return StockData.get_portfolio_history(_db, user_id, time_period)

# Function for loading the portfolio page once user is logged in
def portfolio_page():
    st.title('Portfolio Overview')

    db = get_database()
    
    # Time period selector in a smaller column
    col1, col2 = st.columns([1, 3])
    with col1:
        time_periods = {
            '3 Days': '3d',
            '5 Days': '5d',
            '1 Month': '1m',
            '6 Months': '6m',
            '1 Year': '1y'
        }
        selected_period = st.selectbox(
            "Time Period",
            options=list(time_periods.keys()),
            index=4  # Default to 1 Year
        )
    
    # Create placeholders for content
    chart_placeholder = st.empty()
    
    # Show loading message while fetching data
    with st.spinner('Loading portfolio data...'):
        hist_portfolio = fetch_portfolio_history(
            db, 
            st.session_state.user['id'], 
            time_periods[selected_period]
        )
    
    if not hist_portfolio.empty:
        with chart_placeholder:
            # Create interactive chart with multiple traces
            fig = go.Figure()
            
            # Add invested amount line
            fig.add_trace(go.Scatter(
                x=hist_portfolio['timestamp'],
                y=hist_portfolio['invested'],
                mode='lines',
                name='Invested Amount',
                line=dict(color='rgb(49, 130, 189)', width=2)
            ))
            
            # Add market value line
            fig.add_trace(go.Scatter(
                x=hist_portfolio['timestamp'],
                y=hist_portfolio['market_value'],
                mode='lines',
                name='Market Value',
                line=dict(color='rgb(204, 204, 204)', width=2)
            ))
            
            # Add profit/loss area
            fig.add_trace(go.Scatter(
                x=hist_portfolio['timestamp'],
                y=hist_portfolio['profit_loss'],
                mode='lines',
                name='Profit/Loss',
                fill='tozeroy',
                line=dict(color='rgb(50, 171, 96)', width=1)
            ))
            
            fig.update_layout(
                title=f'Portfolio Performance - {selected_period}',
                xaxis_title='Date',
                yaxis_title='Value ($)',
                template='plotly_dark',
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Add summary metrics
        latest = hist_portfolio.iloc[-1]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Total Invested",
                value=f"${latest['invested']:.2f}",
            )
        
        with col2:
            st.metric(
                label="Current Value",
                value=f"${latest['market_value']:.2f}",
            )
        
        with col3:
            profit_loss = latest['profit_loss']
            st.metric(
                label="Total Profit/Loss",
                value=f"${profit_loss:.2f}",
                delta=f"{(profit_loss/latest['invested']*100 if latest['invested'] != 0 else 0):.2f}%"
            )
    
    # Get portfolio data
    portfolio = fetch_portfolio_data(db, st.session_state.user['id'])
    
    st.markdown('---')

    # Process and display stock portfolio
    if portfolio:
        st.markdown("<h1 style='text-align: center;'>STOCKS</h1>", unsafe_allow_html=True)
        
        with st.spinner('Loading current holdings'):
            # Prepare symbols for batch fetching
            stock_symbols = [symbol for symbol, _, _ in portfolio]
            stock_prices = fetch_current_prices(stock_symbols)
            
            portfolio_data = []
            # Here we are calling the get stock data function and the function returns historic data in form of a dataframe
            for symbol, shares, avg_price in portfolio:
                if symbol in stock_prices:
                    current_price = stock_prices[symbol]
                    position_value = shares * current_price
                    profit_loss = (current_price - avg_price) * shares
                    profit_loss_pct = ((current_price - avg_price) / avg_price) * 100
                    
                    portfolio_data.append({
                        'Symbol': symbol,
                        'Shares': f"{shares:,.2f}",
                        'Avg Price': f'${avg_price:,.2f}',
                        'Current Price': f'${current_price:,.2f}',
                        'Value': f'${position_value:,.2f}',
                        'raw_profit_loss': profit_loss,
                        'raw_profit_loss_pct': profit_loss_pct,
                        'Profit/Loss': f'${profit_loss:,.2f} ({profit_loss_pct:.2f}%)'
                    })
            
            if portfolio_data:
                create_asset_cards(portfolio_data)
    else:
        st.info('Your portfolio is empty. Start trading to build your portfolio!')

    st.markdown('---')
    st.markdown("<h1 style='text-align: center;'>CRYPTO</h1>", unsafe_allow_html=True)

    # Process and display crypto portfolio
    crypto_retrieved_data = fetch_crypto_data(db, st.session_state.user['id'])

    if crypto_retrieved_data:
        with st.spinner('Loading current holdings'):
            # Prepare symbols for batch fetching
            crypto_symbols = [symbol for symbol, _, _ in crypto_retrieved_data]
            crypto_prices = fetch_crypto_prices(crypto_symbols)
            
            crypto_data = []
            for symbol, crypto_amount, avg_price in crypto_retrieved_data:
                if symbol in crypto_prices:
                    current_price = crypto_prices[symbol]
                    position_value = current_price * crypto_amount
                    profit_loss = (current_price - avg_price) * crypto_amount
                    profit_loss_pct = ((current_price - avg_price) / avg_price) * 100

                    crypto_data.append({
                        'Symbol': symbol,
                        'Crypto Amount': f"{crypto_amount:,.2f}",
                        'Avg Price': f'${avg_price:,.2f}',
                        'Current Price': f'${current_price:,.2f}',
                        'Value': f'${position_value:,.2f}',
                        'raw_profit_loss': profit_loss,
                        'raw_profit_loss_pct': profit_loss_pct,
                        'Profit/Loss': f'${profit_loss:,.2f} ({profit_loss_pct:.2f}%)'
                    })
            
            if crypto_data:
                create_asset_cards(crypto_data)
            else:
                st.info('Your portfolio is empty. Start trading to build your portfolio!')

def create_asset_cards(data):
    # CSS styles for the cards
    st.markdown("""
    <style>
        .stock-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.2rem;
            padding: 1.2rem;
            margin: 0 auto;
        }
        .stock-card {
            background: linear-gradient(145deg, #1a1f2c, #2a2f3c);
            border: 1px solid #2d3748;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 0.7rem;
            transition: all 0.3s ease;
        }
        .stock-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
            border-color: #805ad5;
        }
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.2rem;
            padding-bottom: 0.7rem;
            border-bottom: 1px solid rgba(99, 108, 138, 0.3);
        }
        .stock-symbol {
            font-size: 1.4rem;
            font-weight: 700;
            color: #805ad5;
            text-shadow: 0 0 15px rgba(128, 90, 213, 0.3);
        }
        .stock-price-info {
            text-align: right;
        }
        .stock-current-price {
            font-size: 1.6rem;
            font-weight: bold;
            color: #e2e8f0;
            margin-bottom: 0.6rem;
            text-shadow: 0 0 10px rgba(226, 232, 240, 0.2);
        }
        .stock-change {
            font-size: 1rem;
            padding: 0.3rem 1rem;
            border-radius: 999px;
            display: inline-block;
            font-weight: 600;
        }
        .stock-info {
            display: grid;
            gap: 0.7rem;
            background: rgba(26, 32, 44, 0.4);
            padding: 1rem;
            border-radius: 12px;
        }
        .stock-line {
            display: flex;
            justify-content: space-between;
            padding: 0.4rem 0;
            color: #a0aec0;
            font-size: 1rem;
        }
        .positive {
            color: #48bb78;
            background: rgba(72, 187, 120, 0.1);
            border: 1px solid rgba(72, 187, 120, 0.2);
        }
        .negative {
            color: #f56565;
            background: rgba(245, 101, 101, 0.1);
            border: 1px solid rgba(245, 101, 101, 0.2);
        }
        .label {
            font-weight: 500;
        }
        .value {
            font-weight: 600;
            color: #e2e8f0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Start grid container
    st.markdown('<div class="stock-grid">', unsafe_allow_html=True)
    
    # Create cards for each asset
    for asset in data:
        profit_loss = asset['raw_profit_loss']
        profit_loss_pct = asset['raw_profit_loss_pct']
        is_profit = profit_loss >= 0
        
        # Determine which quantity label to use (Shares or Amount)
        quantity_label = 'Amount' if 'Crypto Amount' in asset else 'Shares'
        quantity_value = asset.get('Crypto Amount', asset.get('Shares'))
        
        card_html = f"""
            <div class="stock-card">
                <div class="stock-header">
                    <div class="stock-symbol">{asset['Symbol']}</div>
                    <div class="stock-price-info">
                        <span class="stock-current-price">{asset['Current Price']}</span>
                        <span class="stock-change {'positive' if is_profit else 'negative'}">
                            {profit_loss_pct:.2f}%
                        </span>
                    </div>
                </div>
                <div class="stock-info">
                    <div class="stock-line">
                        <span class="label">{quantity_label}</span>
                        <span class="value">{quantity_value}</span>
                    </div>
                    <div class="stock-line">
                        <span class="label">Avg Price</span>
                        <span class="value">{asset['Avg Price']}</span>
                    </div>
                    <div class="stock-line">
                        <span class="label">Market Value</span>
                        <span class="value">{asset['Value']}</span>
                    </div>
                    <div class="stock-line">
                        <span class="label">P/L</span>
                        <span class="value {'positive' if is_profit else 'negative'}">
                            ${profit_loss:,.2f} ({profit_loss_pct:.2f}%)
                        </span>
                    </div>
                </div>
            </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    # Close grid container
    st.markdown('</div>', unsafe_allow_html=True)