import streamlit as st

# Function to load Registration page
def register_page(db):
    st.title('Register New Account')

    # form to register a new user
    with st.form('register_form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        submitted = st.form_submit_button('Register')

    # if the submitted button is pressed
    if submitted:
        # If both password matches
        if password != confirm_password:
            st.error('Passwords do not match')
        # if all the fields are entered
        elif not all([name, email, password]):
            st.error('All fields are required')
        else:
            # Calling the add_user function from the database class
            user_id = db.add_user(name, email, password)
            if user_id:
                st.success('Registration successful! Please Login.')
                st.session_state.current_page = 'login'
                st.rerun()
            else:
                st.error('Registration failed. Email might already be registered.')

# Function to load the login page
def login_page(db):
    st.title('📈 Trading Platform')
    
    with st.form('login_form'):
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Login')

        if submitted:
            user = db.verify_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.current_page = 'trading'
                st.rerun()
            else:
                st.error('Invalid email or password')
    
    if st.button('Register New Account'):
        st.session_state.current_page = 'register'  # If the register new account button is clicked, the page will be loaded to register page.
        st.rerun()

# Function to logout
def logout():
    st.session_state.logged_in = False
    st.session_state.current_page = 'login'
    st.session_state.user = None  # This will forget the user