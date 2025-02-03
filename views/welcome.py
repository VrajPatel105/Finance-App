import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from streamlit.components.v1 import html


def create_feature_card(icon, title, description):
    return f'''
        <div class="feature-card" style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border-radius: 20px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <h3 style="color: #6366f1; font-size: 1.25rem; margin-bottom: 0.5rem;">
                {title}
            </h3>
            <p style="color: #94a3b8;">
                {description}
            </p>
        </div>
    '''

def create_stat_card(label, value, change):
    return f'''
        <div style="
            background: rgba(30, 41, 59, 0.5);
            border-radius: 16px;
            padding: 1.25rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <div style="font-size: 0.875rem; color: #94a3b8;">{label}</div>
            <div style="font-size: 1.5rem; color: #6366f1; font-weight: 600;">{value}</div>
            <div style="font-size: 0.875rem; color: #22c55e;">↑ {change}</div>
        </div>
    '''

def welcome_page():
    # Base styles
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
        }
        
        .hero-section {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 32px;
            padding: 3rem 2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .modern-button {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            border: none;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .modern-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }
        
        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section with functional buttons
    st.markdown('''
        <div class="hero-section">
            <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; color: white;">
                Welcome to Finch
            </h1>
            <p style="font-size: 1.25rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 2rem;">
                Elevate Your Trading Experience with AI-Powered Insights
            </p>
        </div>
    ''', unsafe_allow_html=True)

    login_col, register_col = st.columns(2)

    with login_col:
        if st.button("🔐 Login", key="login_button", use_container_width=True, type="primary"):
            st.session_state.current_page = 'login'
            st.rerun()

    with register_col:
        if st.button("✨ Register", key="register_button", use_container_width=True):
            st.session_state.current_page = 'register'
            st.rerun()

    st.markdown("""
        <script>
            function moveButtons() {
                var loginButton = document.querySelector('button[kind="primary"]');
                var registerButton = document.querySelector('button:not([kind="primary"])');
                document.getElementById('login-button').appendChild(loginButton);
                document.getElementById('register-button').appendChild(registerButton);
            }
            setTimeout(moveButtons, 100);
        </script>
    """, unsafe_allow_html=True)


    # Main Content Layout
    col1, col2 = st.columns([5, 7])

    with col1:
        # Feature Cards using container
        features_container = st.container()
        
        # Feature 1
        features_container.markdown(
            create_feature_card(
                "🚀",
                "Smart Trading",
                "AI-powered insights and real-time market analysis to optimize your trades"
            ),
            unsafe_allow_html=True
        )
        
        # Feature 2
        features_container.markdown(
            create_feature_card(
                "📊",
                "Advanced Analytics",
                "Professional-grade tools and detailed market analysis at your fingertips"
            ),
            unsafe_allow_html=True
        )
        
        # Feature 3
        features_container.markdown(
            create_feature_card(
                "🛡️",
                "Enterprise Security",
                "Bank-grade encryption and advanced security protocols to protect your assets"
            ),
            unsafe_allow_html=True
        )

    with col2:
        # Chart Data
        dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30, 0, -1)]
        base_price = 100
        prices = [base_price + np.random.normal(0, 2) + (i/8) for i in range(30)]
        
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=dates,
            open=[p * (1 - np.random.uniform(0, 0.02)) for p in prices],
            high=[p * (1 + np.random.uniform(0, 0.03)) for p in prices],
            low=[p * (1 - np.random.uniform(0, 0.03)) for p in prices],
            close=prices,
            increasing_line_color='#22c55e',
            decreasing_line_color='#ef4444',
            name='Price'
        ))

        # Moving averages
        ma7 = np.convolve(prices, np.ones(7)/7, mode='valid')
        ma21 = np.convolve(prices, np.ones(21)/21, mode='valid')

        fig.add_trace(go.Scatter(
            x=dates[6:],
            y=ma7,
            line=dict(color='#6366f1', width=1.5),
            name='7-day MA'
        ))

        fig.add_trace(go.Scatter(
            x=dates[20:],
            y=ma21,
            line=dict(color='#8b5cf6', width=1.5),
            name='21-day MA'
        ))

        fig.update_layout(
            title={
                'text': "Live Market Analysis",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24, 'color': '#f8fafc'}
            },
            template='plotly_dark',
            height=500,
            paper_bgcolor='rgba(30, 41, 59, 0.3)',
            plot_bgcolor='rgba(30, 41, 59, 0.3)',
            xaxis_rangeslider_visible=False,
            margin=dict(l=20, r=20, t=60, b=20),
            font={'color': '#f8fafc'},
            xaxis_gridcolor='rgba(255, 255, 255, 0.1)',
            yaxis_gridcolor='rgba(255, 255, 255, 0.1)',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(30, 41, 59, 0.7)'
            )
        )

        # Display chart
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Stats Section using columns
        st.markdown("""
            <style>
            .stat-card {
                background: rgba(30, 41, 59, 0.5);
                border-radius: 16px;
                padding: 1.25rem;
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin: 0.5rem 0;
            }
            </style>
        """, unsafe_allow_html=True)
        
        stat1, stat2, stat3 = st.columns(3)
        
        with stat1:
            st.markdown("""
                <div class="stat-card">
                    <div style="font-size: 0.875rem; color: #94a3b8;">24h Volume</div>
                    <div style="font-size: 1.5rem; color: #6366f1; font-weight: 600;">$18.5M</div>
                    <div style="font-size: 0.875rem; color: #22c55e;">↑ 12.3%</div>
                </div>
            """, unsafe_allow_html=True)
            
        with stat2:
            st.markdown("""
                <div class="stat-card">
                    <div style="font-size: 0.875rem; color: #94a3b8;">Market Cap</div>
                    <div style="font-size: 1.5rem; color: #6366f1; font-weight: 600;">$245.8M</div>
                    <div style="font-size: 0.875rem; color: #22c55e;">↑ 8.7%</div>
                </div>
            """, unsafe_allow_html=True)
            
        with stat3:
            st.markdown("""
                <div class="stat-card">
                    <div style="font-size: 0.875rem; color: #94a3b8;">Active Traders</div>
                    <div style="font-size: 1.5rem; color: #6366f1; font-weight: 600;">12.4K</div>
                    <div style="font-size: 0.875rem; color: #22c55e;">↑ 5.2%</div>
                </div>
            """, unsafe_allow_html=True)

    # Why Choose Finch Section
    st.markdown('''
        <div style="background: rgba(30, 41, 59, 0.7); border-radius: 24px; padding: 2rem; margin: 2rem 0;">
            <h2 style="color: #f8fafc; font-size: 2rem; text-align: center; margin-bottom: 2rem;">
                Why Choose Finch?
            </h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
    ''', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_feature_card("💡", "AI-Powered", 
                   "Advanced algorithms for smarter trading "), unsafe_allow_html=True)
    with col2:
        st.markdown(create_feature_card("⚡", "Real-Time", 
                   "Instant market updates and notifications"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_feature_card("🎯", "Precision", 
                   "Accurate analysis and predictions"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_feature_card("🔒", "Secure", 
                   "Enterprise-grade security protocols"), unsafe_allow_html=True)


    st.markdown("""
        <style>
        .cta-container {
            background: rgba(30, 41, 59, 0.7);
            border-radius: 24px;
            padding: 2rem;
            text-align: center;
            margin-top: 2rem;
            margin-bottom : 1.5rem;
        }
        .cta-title {
            color: #f8fafc;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .cta-text {
            color: #94a3b8;
            font-size: 1.125rem;
            margin-bottom: 2rem;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 1rem;
        }
        .stButton > button {
            width: 100%;
            border-radius: 20px;
            height: 3rem;
            font-size: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="cta-container">
            <h2 class="cta-title">Ready to Start Trading?</h2>
            <p class="cta-text">Join thousands of successful traders on Finch</p>
            <div class="button-container">
                <div id="login-button"></div>
                <div id="register-button"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    