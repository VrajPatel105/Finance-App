import streamlit as st
import plotly.graph_objects as go
from models.stock import StockData
from database.db_manager import Database
import requests

# Function for loading the portfolio page once user is logged in
def portfolio_page():
    st.title('Portfolio Overview')

    db = Database()
    
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
    
    # Get current portfolio holdings for the specific user.
    portfolio = db.get_portfolio(st.session_state.user['id'])
    
    # Create a placeholder for the chart
    chart_placeholder = st.empty()
    
    # Show loading message while fetching data
    with st.spinner('Loading portfolio data...'):
        hist_portfolio = StockData.get_portfolio_history(
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
    
    # Displaying the current holdings of the user with styled cards

    st.markdown('---')


    if portfolio:
        st.subheader("Current Holdings")
        st.markdown("<h1 style='text-align: center;'>STOCKS</h1>", unsafe_allow_html=True)
        
        # Show loading message while fetching current holdings data
        with st.spinner('Loading current holdings...'):
            portfolio_data = []
            # Here we are calling the get stock data function and the function returns historic data in form of a dataframe and the second this is _ because we need it.
            for symbol, shares, avg_price in portfolio:
                hist_data, _ = StockData.get_stock_data(symbol, period='1d')
                if hist_data is not None and not hist_data.empty:
                    current_price = hist_data['Close'].iloc[-1] # Since hist_data is a dataframe, we are fetching the last row by iloc[-1] in the 'Close' column
                    position_value = shares * current_price
                    profit_loss = (current_price - avg_price) * shares
                    profit_loss_pct = ((current_price - avg_price) / avg_price) * 100
                    
                    # Appending all the above defined value into a dataframe and then plotting the stock cards ( This are for the stocks that are owned by the user)
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
                create_stock_cards_stock(portfolio_data)
    else:
        st.info('Your portfolio is empty. Start trading to build your portfolio!')


    st.markdown('---')
    st.markdown("<h1 style='text-align: center;'>CRYPTO</h1>", unsafe_allow_html=True)


    crypto_retrieved_data = db.get_crypto_data(st.session_state.user['id'])

    if crypto_retrieved_data:
        with st.spinner('Loading current holdings...'):
            crypto_data = []

        for symbol,crypto_amount, avg_price in crypto_retrieved_data:

           headers = {
           'X-CMC_PRO_API_KEY': '440c12ff-74f9-4ff9-92a1-07345791e1cb',
           'Accept': 'application/json'
           }
            # problem to fix: This for loop will hit the api everytime for a new symbol. But for now, since we are not going to make a lot of calls, it's not a problem.
           response = requests.get(
               'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
               headers=headers,
               params={'symbol': symbol}
           )
           data = response.json()

           current_price = data['data'][symbol]['quote']['USD']['price']
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
        
        if crypto_retrieved_data:
                create_stock_cards_crypto(crypto_data)
        else:
            st.info('Your portfolio is empty. Start trading to build your portfolio!')


def create_stock_cards_stock(portfolio_data):
        # Html code for styled stock cards
        st.markdown("""
        <style>
            .stock-grid {
                display: grid;
                grid-template-columns: 1fr;
                gap: 1rem;
                padding: 1rem;
                margin: 0 auto;
            }
            .stock-card {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 1.25rem;
                margin-bottom: 0.5rem;
            }
            .stock-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                border-color: #58a6ff;
            }
            .stock-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid rgba(48, 54, 61, 0.5);
            }
            .stock-symbol {
                font-size: 1.25rem;
                font-weight: bold;
                color: #58a6ff;
            }
            .stock-price-info {
                text-align: right;
            }
            .stock-current-price {
                font-size: 1.5rem;
                font-weight: bold;
                color: #c9d1d9;
                margin-bottom: 0.5rem;
            }
            .stock-change {
                font-size: 1rem;
                padding: 0.25rem 0.75rem;
                border-radius: 999px;
                display: inline-block;
            }
            .stock-info {
                display: grid;
                gap: 0.5rem;
            }
            .stock-line {
                display: flex;
                justify-content: space-between;
                padding: 0.25rem 0;
                color: #8b949e;
                font-size: 0.9rem;
            }
            .positive {
                color: #238636;
                background: rgba(35, 134, 54, 0.1);
            }
            .negative {
                color: #f85149;
                background: rgba(248, 81, 73, 0.1);
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Start grid container
        st.markdown('<div class="stock-grid">', unsafe_allow_html=True)
        
        # Creating seperate cards for every entry of the user's portfolio (stocks)
        for stock in portfolio_data:
            profit_loss = stock['raw_profit_loss']
            profit_loss_pct = stock['raw_profit_loss_pct']
            is_profit = profit_loss >= 0
            
            card_html = f"""
                <div class="stock-card">
                    <div class="stock-header">
                        <div class="stock-symbol">{stock['Symbol']}</div>
                        <div class="stock-price-info">
                            <span class="stock-current-price">{stock['Current Price']}</span>
                            <span class="stock-change {'positive' if is_profit else 'negative'}">
                                {profit_loss_pct:.2f}%
                            </span>
                        </div>
                    </div>
                    <div class="stock-info">
                        <div class="stock-line">
                            <span class="label">Shares</span>
                            <span class="value">{stock['Shares']}</span>
                        </div>
                        <div class="stock-line">
                            <span class="label">Avg Price</span>
                            <span class="value">{stock['Avg Price']}</span>
                        </div>
                        <div class="stock-line">
                            <span class="label">Market Value</span>
                            <span class="value">{stock['Value']}</span>
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


def create_stock_cards_crypto(crypto_data):
    # Html code for styled crypto cards with new design
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
    
    # Creating separate cards for every entry of the user's portfolio (crypto)
    for crypto in crypto_data:
        profit_loss = crypto['raw_profit_loss']
        profit_loss_pct = crypto['raw_profit_loss_pct']
        is_profit = profit_loss >= 0
        
        card_html = f"""
            <div class="stock-card">
                <div class="stock-header">
                    <div class="stock-symbol">{crypto['Symbol']}</div>
                    <div class="stock-price-info">
                        <span class="stock-current-price">{crypto['Current Price']}</span>
                        <span class="stock-change {'positive' if is_profit else 'negative'}">
                            {profit_loss_pct:.2f}%
                        </span>
                    </div>
                </div>
                <div class="stock-info">
                    <div class="stock-line">
                        <span class="label">Amount</span>
                        <span class="value">{crypto['Crypto Amount']}</span>
                    </div>
                    <div class="stock-line">
                        <span class="label">Avg Price</span>
                        <span class="value">{crypto['Avg Price']}</span>
                    </div>
                    <div class="stock-line">
                        <span class="label">Market Value</span>
                        <span class="value">{crypto['Value']}</span>
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