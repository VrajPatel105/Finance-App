import streamlit as st
from database.db_manager import Database
from views.auth import register_page, login_page, logout
from views.welcome import welcome_page
from views.trading import trading_page
from views.portfolio import portfolio_page

# Function to load a side bar containing a portfolio, trade and logout button
def create_sidebar():
    with st.sidebar:
        st.title('Navigation')
        st.write(f"Welcome, {st.session_state.user['name']}!")
        st.metric(
            label="Available Balance",
            value=f"${st.session_state.user['balance']:.2f}",
            delta=f"${st.session_state.user['balance'] - 100000:.2f}"
        )
        
        # checking which button is pressed and changing the current page based on that
        if st.button('📊 Portfolio'):
            st.session_state.current_page = 'portfolio'
        if st.button('💱 Trade'):
            st.session_state.current_page = 'trading'
        
        st.sidebar.button('🚪 Logout', on_click=logout)  # if it's clicked, it will call the logout function

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    if 'user' not in st.session_state:
        st.session_state.user = None

def main():
    st.set_page_config(
        page_title="Trading Platform",
        page_icon="📈",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()

    db = Database()  # An instance of Database class

    if not st.session_state.logged_in:
        if st.session_state.current_page == 'welcome':
            welcome_page()
        elif st.session_state.current_page == 'register':
            register_page(db)
        else:
            login_page(db)
    else:
        create_sidebar()
        if st.session_state.current_page == 'portfolio':
            portfolio_page()
        else:
            trading_page()

if __name__ == "__main__":
    main()