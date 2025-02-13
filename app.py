import streamlit as st

st.set_page_config(
       page_title="Finch",
       page_icon='resources/finch.ico',
       layout="wide"
   )

st.markdown("""
   <style>
       .stApp {
           background: rgb(0, 0, 0);
           color: #E2E8F0;
       }
       
       /* Username card */
       .user-name {
           background: #1F1F1F;
           border: 1px solid #A855F7;
           border-radius: 12px;
           padding: 12px 20px;
           color: #E2E8F0;
           font-weight: 600;
           letter-spacing: 0.5px;
           box-shadow: 0 0 10px rgba(168, 85, 247, 0.2);
       }
       
       /* Balance card */
       .custom-metric {
           background: #1F1F1F;
           border: 2px solid #A855F7;
           box-shadow: 0 0 20px #A855F7;
           border-radius: 16px;
           padding: 25px;
           margin: 20px 0;
       }
       
       .metric-label {
           color: #A855F7;
           font-size: 0.9rem;
           text-transform: uppercase;
           letter-spacing: 2px;
           margin-bottom: 15px;
       }
       
       .metric-value {
           font-size: 2.5rem;
           font-weight: 800;
           background: linear-gradient(to right, #E2E8F0, #A855F7);
           -webkit-background-clip: text;
           -webkit-text-fill-color: transparent;
           margin: 10px 0;
       }
       
       .metric-delta {
           background: rgba(168, 85, 247, 0.1);
           border: 1px solid rgba(168, 85, 247, 0.3);
           border-radius: 20px;
           padding: 5px 15px;
           font-size: 0.9rem;
           color: #E2E8F0;
       }
       
       /* Navigation buttons */
       .stButton > button {
           background: #1F1F1F;
           border: 1px solid #A855F7;
           border-radius: 12px;
           color: #E2E8F0;
           padding: 12px 24px;
           font-size: 1rem;
           font-weight: 500;
           letter-spacing: 0.5px;
           transition: all 0.2s;
           text-align: left;
           width: 100%;
           display: flex;
           align-items: center;
           margin-bottom: 12px;
           position: relative;
           overflow: hidden;
       }
       
       .stButton > button::after {
           content: '';
           position: absolute;
           top: 0;
           left: 0;
           width: 100%;
           height: 100%;
           background: linear-gradient(45deg, transparent, rgba(168, 85, 247, 0.1), transparent);
           transform: translateX(-100%);
           transition: 0.5s;
       }
       
       .stButton > button:hover {
           box-shadow: 0 0 15px #A855F7;
           background: #2D2D2D;
       }
       
       .stButton > button:hover::after {
           transform: translateX(100%);
       }
   </style>
""", unsafe_allow_html=True)


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
   balance = st.session_state.user['balance']
   delta = balance - 100000 
   
   st.markdown(f"""
   <div style="text-align: center;">
       <div style="font-size: 3rem; font-weight: 800; background: linear-gradient(to right, #E2E8F0, #A855F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;">
           ${balance:,.2f}
       </div>
       <div style="font-size: 0.9rem; color: #E2E8F0; margin-top: -5px;">
           {'↑' if delta >= 0 else '↓'} ${abs(delta):,.2f}
       </div>
   </div>
   """, unsafe_allow_html=True)


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