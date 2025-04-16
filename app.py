import streamlit as st
import json 
# We are setting the page config here.
# At the top of app.py 
st.set_page_config( 
    page_title="Finch",  
    page_icon='resources/finch.ico', 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None, 
        'Report a bug': None,
        'About': None
    }
)
# importing all the libraries and functions from other classes.
from database.connection import get_database
from views.auth import register_page, login_page, logout
from views.welcome import welcome_page
from views.trading import trading_page
from views.portfolio import portfolio_page
from views.crypto import load_crypto
from views.ai_assistant import Assistant
from views.news import load_news
from views.music import create_floating_music_player
from views.account import account_page

# css for user info
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

def load_user_info():
   # Fetching the user's balance from session state.
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
# Function for creating sidebar.
def create_sidebar():
    with st.sidebar:
       # loading the user info function.
        load_user_info()
       # loading spotify song grid from music.py.
       # This music player sticks with the sidebar.
        create_floating_music_player()
    
        
        st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        padding: 16px 24px;
        background: linear-gradient(to right, #15326d, #1e4fd8);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.125rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        margin-bottom: 16px;
        transition: all 0.3s;
        box-shadow: 0 4px 6px -1px rgba(30, 79, 216, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(to right, #122a5c, #15326d);
        box-shadow: 0 8px 12px -3px rgba(30, 79, 216, 0.25);
    }
    
    .stButton > button span:first-child {
        transition: transform 0.3s;
    }
    
    .stButton > button:hover span:first-child {
        transform: scale(1.1);
    }
    </style>
""", unsafe_allow_html=True)

           # Buttons to load in the sidebar.
           # Here we are also maintaining user session state by using a current page to keep a track on which page is the user currently on.
           # We use the streamlit inbuild save session state funciton to save the session. This will keep the user logged in until not logged out.
        if st.button('💱 Stocks', key='stocks_button'):
            st.session_state.current_page = 'trading'
            save_session_state()
            st.rerun()
        
        if st.button('🌐 Crypto', key='crypto_button'):
            st.session_state.current_page = 'crypto'
            save_session_state()
            st.rerun()
        
        if st.button('📊 Portfolio', key='portfolio_button'):
            st.session_state.current_page = 'portfolio'
            save_session_state()
            st.rerun()

        if st.button('🤖 AI Assistant', key='ai_button'):
            st.session_state.current_page = 'ai_assistant'
            save_session_state()
            st.rerun()

        if st.button('📰 News', key='news_button'):
            st.session_state.current_page = 'news'
            save_session_state()
            st.rerun()

        if st.button('👤 Account', key='account_button'):
            st.session_state.current_page = 'account'
            save_session_state()
            st.rerun()
                        
        st.sidebar.button('🚪 Logout', on_click=logout)

def save_session_state():
    if st.session_state.logged_in:
        state_data = {
            'logged_in': st.session_state.logged_in,
            'current_page': st.session_state.current_page,
            'user': st.session_state.user
        }
        st.query_params['session_state'] = json.dumps(state_data)

def init_session_state():
    # Trying to load saved state from query params first
    try:
        saved_state = st.query_params.get('session_state')
        if saved_state:
            state_data = json.loads(saved_state)
            st.session_state.logged_in = state_data.get('logged_in', False)
            st.session_state.current_page = state_data.get('current_page', 'welcome')
            st.session_state.user = state_data.get('user', None)
        else:
            if 'logged_in' not in st.session_state:
                st.session_state.logged_in = False
            if 'current_page' not in st.session_state:
                st.session_state.current_page = 'welcome'
            if 'user' not in st.session_state:
                st.session_state.user = None
    except:
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'welcome'
        if 'user' not in st.session_state:
            st.session_state.user = None
            
    # Initialize AI chat history if not present
    if 'ai_chat_history' not in st.session_state:
        st.session_state.ai_chat_history = []

def main():
    init_session_state()
    st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background-color: #00000;
    }
    
    /* Ensure text is visible */
    .stMarkdown {
        color: #FAFAFA;
    }
    
    /* Enable webkit features globally */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    </style>
""", unsafe_allow_html=True)
       
       # Calling the database instance
    db = get_database()

    if st.session_state.logged_in and 'user' in st.session_state:
    # Verify balance is in sync at the start of each page load
        db.verify_and_sync_balance(st.session_state.user['id'])

    # Check for Enter key press to prevent page change
    for key in st.session_state.keys():
        if key.startswith('formsubmit'):
            st.session_state[key] = False

       # calling the functions based on the user's current page. And if user don't have any current page, then it will load the welcome page.
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
        save_session_state()  # Save state after confirming logged in
        
        if st.session_state.current_page == 'portfolio':
            portfolio_page()
        elif st.session_state.current_page == 'crypto':
            load_crypto()
        elif st.session_state.current_page == 'ai_assistant':
            ai = Assistant()
            ai.run()
        elif st.session_state.current_page == 'news':
            load_news()
        elif st.session_state.current_page == 'account':
            account_page()
        else:
            trading_page()

if __name__ == "__main__":
    main()
