import streamlit as st

st.set_page_config(
       page_title="Trading Platform",
       page_icon='resources/finch.ico',
       layout="wide"
   )
from database.connection import get_database
from views.auth import register_page, login_page, logout
from views.welcome import welcome_page
from views.trading import trading_page
from views.portfolio import portfolio_page
from views.crypto import load_crypto
from views.ai_assistant import Assistant
from views.news import load_news

# Function to load a side bar containing a portfolio, trade and logout button


def load_user_info():

    st.markdown(f"""
    <div style="
        font-size: 0.9rem;
        color: #4a5568;
        font-weight: 500;
        margin-bottom: 8px;
        padding: 10px 18px;
        background-color: #e2e8f0;
        border-radius: 20px;
        display: inline-block;
    ">
         {st.session_state.user['name']}!
    </div>
""", unsafe_allow_html=True)


    st.markdown("""
    <style>
    .custom-metric {
        background: linear-gradient(to right, #15326d, #1e4fd8);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(30, 79, 216, 0.1);
        text-align: center;
    }
    .custom-metric .metric-label {
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .custom-metric .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 16px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .custom-metric .metric-delta {
        font-size: 1rem;
        margin-top: 12px;
        display: inline-block;
        padding: 4px 8px;
        border-radius: 20px;
        background-color: rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    balance = st.session_state.user['balance']
    delta = balance - 100000

    st.markdown(f"""
        <div class="custom-metric">
            <div class="metric-label">Available Balance</div>
            <div class="metric-value">${balance:,.2f}</div>
            <div class="metric-delta">{'↑' if delta >= 0 else '↓'} ${abs(delta):,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add spacer
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)



def create_sidebar():
    with st.sidebar:
        load_user_info()
        
        st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        padding: 16px 24px;
        background: linear-gradient(to right, #15326d, #1e4fd8);  /* Darker blue shades */
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.125rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        margin-bottom: 16px;
        transition: all 0.3s;
        box-shadow: 0 4px 6px -1px rgba(30, 79, 216, 0.1);  /* Adjusted shadow color */
    }
    
    .stButton > button:hover {
        background: linear-gradient(to right, #122a5c, #15326d);  /* Darker blue shades for hover */
        box-shadow: 0 8px 12px -3px rgba(30, 79, 216, 0.25);  /* Adjusted shadow color */
    }
    
    .stButton > button span:first-child {
        transition: transform 0.3s;
    }
    
    .stButton > button:hover span:first-child {
        transform: scale(1.1);
    }
    </style>
""", unsafe_allow_html=True)

        if st.button('💱 Stocks'):
            st.session_state.current_page = 'trading'
        
        if st.button('🌐 Crypto'):
            st.session_state.current_page = 'crypto'
        
        if st.button('📊 Portfolio'):
            st.session_state.current_page = 'portfolio'

        if st.button('🤖 AI Assistant'):
            st.session_state.current_page = 'ai_assistant'

        if st.button('News'):
            st.session_state.current_page = 'news'
                        
        st.sidebar.button('🚪 Logout', on_click=logout)


def init_session_state():
   if not hasattr(st.session_state, 'logged_in'):
       st.session_state.logged_in = False
   if not hasattr(st.session_state, 'current_page'):
       st.session_state.current_page = 'welcome'
   if not hasattr(st.session_state, 'user'):
       st.session_state.user = None
   if not hasattr(st.session_state, 'ai_chat_history'):
       st.session_state.ai_chat_history = []

def main():
   
   init_session_state()
   db = get_database()

   if not st.session_state.logged_in:
       if st.session_state.current_page == 'register':
           register_page(db)
       elif st.session_state.current_page == 'login':
           login_page(db)
       elif st.session_state.current_page == 'crypto':
           load_crypto()
       else:
           welcome_page()
   else:
       create_sidebar()
       if st.session_state.current_page == 'portfolio':
           portfolio_page()
       elif st.session_state.current_page == 'crypto':
           load_crypto()
       elif st.session_state.current_page == 'ai_assistant':
           ai = Assistant()
           ai.run()
       elif st.session_state.current_page == 'news':
            load_news()
       else:
           trading_page()

if __name__ == "__main__":
   main()