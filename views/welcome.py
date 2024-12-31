import streamlit as st
import plotly.graph_objects as go

# A simple Function for loading the welcome page.
def welcome_page():
    st.title("Welcome to Trading Platform 📈")
    
    # Create a two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Start Your Trading Journey Today!
        
        Our platform offers:
        * Real-time market data
        * Portfolio tracking
        * Historical price analysis
        * User-friendly interface
        
        Join thousands of traders who trust our platform for their investment needs.
        """)
        
        # Add login and register buttons
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            if st.button("Login", type="primary", use_container_width=True):
                st.session_state.current_page = 'login'
                st.rerun()
        with col1_2:
            if st.button("Register", use_container_width=True):
                st.session_state.current_page = 'register'
                st.rerun()
    
    # A chart on the welcome page
    with col2:
        # Create a sample chart for visualization
        fig = go.Figure(data=[go.Candlestick(
            x=['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
            open=[100, 102, 104, 101, 105],
            high=[104, 107, 108, 105, 108],
            low=[99, 100, 101, 99, 102],
            close=[102, 104, 101, 105, 107]
        )])
        
        fig.update_layout(
            title="Trade Easily and Securely",
            yaxis_title="Stock Price",
            template="plotly_dark",
            height=400
        )
    
        st.plotly_chart(fig, use_container_width=True)