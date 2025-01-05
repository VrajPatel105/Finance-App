import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np


def welcome_page():
    # Custom CSS remains same but adjust some heights
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, #0f172a, #1e293b);
            color: #e2e8f0;
        }
        
        .welcome-header {
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .feature-card {
            background: rgba(30, 41, 59, 0.8);
            padding: 0.8rem;
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
            margin-bottom: 0.7rem;
            transition: transform 0.2s;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.7rem;
            margin: 1rem 0;
        }
        
        .auth-buttons {
            margin-top: 1rem;
        }
        
        .stButton button {
            height: 2.5rem;
            font-size: 1rem;
            font-weight: 500;
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            border: none;
            transition: all 0.3s;
        }
        </style>
    """, unsafe_allow_html=True)

    # Welcome header - made more compact
    st.markdown("""
        <div class="welcome-header">
            <h1 style='font-size: 2rem; font-weight: 600; margin-bottom: 0.5rem;'>Welcome to Finch</h1>
            <p style='font-size: 1rem; opacity: 0.9;'> Where Pennies Grow Wings</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create main layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        # Welcome message and buttons at the top
        st.markdown("""
        <div class="feature-card">
            <h3 style='color: #3b82f6; font-size: 1.2rem;'>🚀 Start Your Trading Journey Today!</h3>
            <p style='font-size: 0.9rem;'>Experience the power of intelligent trading</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login/Register buttons moved up
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("🔐 Login", type="primary", use_container_width=True):
                st.session_state.current_page = 'login'
                st.rerun()
        with col1_2:
            if st.button("✨ Register", use_container_width=True):
                st.session_state.current_page = 'register'
                st.rerun()

        # Features in a 2x2 grid
        st.markdown("""
        <div style='margin-top: 1rem;'>
            <h3 style='color: #3b82f6; font-size: 1.2rem; margin-bottom: 0.5rem;'>Platform Features</h3>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4 style='color: #3b82f6; font-size: 1rem;'>📊 Real-time Data</h4>
                    <p style='font-size: 0.8rem;'>Live market updates</p>
                </div>
                <div class="feature-card">
                    <h4 style='color: #3b82f6; font-size: 1rem;'>💼 Portfolio</h4>
                    <p style='font-size: 0.8rem;'>Track investments easily</p>
                </div>
                <div class="feature-card">
                    <h4 style='color: #3b82f6; font-size: 1rem;'>📈 Analytics</h4>
                    <p style='font-size: 0.8rem;'>Professional tools</p>
                </div>
                <div class="feature-card">
                    <h4 style='color: #3b82f6; font-size: 1rem;'>🔒 Security</h4>
                    <p style='font-size: 0.8rem;'>Enterprise protection</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced chart in column 2
    with col2:
        # Generate sample data
        dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30, 0, -1)]
        base_price = 100
        prices = [base_price + np.random.normal(0, 2) + (i/10) for i in range(30)]
        
        fig = go.Figure(data=[go.Candlestick(
            x=dates,
            open=[p * (1 - np.random.uniform(0, 0.02)) for p in prices],
            high=[p * (1 + np.random.uniform(0, 0.03)) for p in prices],
            low=[p * (1 - np.random.uniform(0, 0.03)) for p in prices],
            close=prices
        )])
        
        # Reduced chart height
        fig.update_layout(
            title={
                'text': "Live Market Trends",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 20, 'color': '#e2e8f0'}
            },
            yaxis_title="Stock Price ($)",
            template="plotly_dark",
            height=400,  # Reduced height
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(30, 41, 59, 0.3)',
            plot_bgcolor='rgba(30, 41, 59, 0.3)',
            xaxis_rangeslider_visible=False,
            font={'color': '#e2e8f0'}
        )
        
        # Add moving averages
        ma20 = np.convolve(prices, np.ones(5)/5, mode='valid')
        fig.add_trace(go.Scatter(
            x=dates[4:],
            y=ma20,
            name='5-day MA',
            line=dict(color='#3b82f6', width=1.5)
        ))

        st.plotly_chart(fig, use_container_width=True)

        # Compact market statistics
        st.markdown("""
        <div class="feature-card" style="margin-top: 0.5rem;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div>
                    <div style="font-size: 0.8rem;">24h Volume</div>
                    <div style="color: #3b82f6; font-size: 1rem;">$12.5M</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem;">Market Cap</div>
                    <div style="color: #3b82f6; font-size: 1rem;">$158.3M</div>
                </div>
                <div>
                    <div style="font-size: 0.8rem;">24h Change</div>
                    <div style="color: #22c55e; font-size: 1rem;">+2.35%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)