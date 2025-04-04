import streamlit as st
import time

# main register page function.
def register_page(db):
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #17171d 100%);
            background-size: 200% 200%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes glow {
            0% { box-shadow: 0 0 20px rgba(168, 85, 247, 0.1); }
            50% { box-shadow: 0 0 30px rgba(168, 85, 247, 0.2); }
            100% { box-shadow: 0 0 20px rgba(168, 85, 247, 0.1); }
        }
        
        .register-container {
            max-width: 500px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(168, 85, 247, 0.1);
            border: 1px solid rgba(168, 85, 247, 0.2);
            backdrop-filter: blur(10px);
            animation: glow 3s ease-in-out infinite;
        }
        
        .register-header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        
        .finch-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #a855f7, #d946ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
        }
        
        .stTextInput input {
            background: rgba(23, 23, 30, 0.9);
            border: 1px solid rgba(168, 85, 247, 0.2);
            color: #f8fafc;
            border-radius: 12px;
            padding: 1rem;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        
        .stTextInput input:focus {
            border-color: #a855f7;
            box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
        }
        
        .stButton button {
            background: linear-gradient(90deg, #7d1cc2, #ab23b3) !important;
            color: white !important;
            border: none !important;
            padding: 1rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-transform: uppercase;
            font-size: 1rem;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(168, 85, 247, 0.3);
        }
        
        .success {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.2);
            color: #22c55e;
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
        }
        
        .error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #ef4444;
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
        }
        
        .login-link {
            text-align: center;
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(23, 23, 30, 0.9);
            border: 1px solid rgba(168, 85, 247, 0.2);
            border-radius: 12px;
        }
        
        .security-features {
            margin-top: 2rem;
            padding: 1.5rem;
            background: rgba(23, 23, 30, 0.9);
            border: 1px solid rgba(168, 85, 247, 0.2);
            border-radius: 12px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
            color: #94a3b8;
        }
        
        .feature-icon {
            color: #a855f7;
            font-size: 1.2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="register-container">
            <div class="register-header">
                <div class="finch-title">Join Finch</div>
                <div class="subtitle">Begin your trading journey today</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.form('register_form'):
        name = st.text_input(
            'Full Name',
            placeholder='Enter your full name'
        )

        email = st.text_input(
            'Email Address',
            placeholder='your.email@example.com'
        )

        col1, col2 = st.columns(2)
        
        with col1:
            password = st.text_input(
                'Create Password',
                type='password',
                placeholder='••••••••'
            )

        with col2:
            confirm_password = st.text_input(
                'Confirm Password',
                type='password',
                placeholder='••••••••'
            )

        submitted = st.form_submit_button('Create Account', use_container_width=True)

    if submitted:
        if password != confirm_password:
            st.error('🔐 Passwords don\'t match')
        elif not all([name, email, password]):
            st.error('📝 Please fill all fields')
        else:
            user_id = db.add_user(name, email, password)
            if user_id:
                st.success('🎉 Account created successfully!')
                time.sleep(1)
                st.session_state.current_page = 'login'
                st.rerun()
            else:
                st.error('📧 Email already registered')

    st.markdown("""
        <div class="login-link">
            <p style="color: #94a3b8; margin-bottom: 1rem;">Already a member?</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button('Sign In to Your Account', use_container_width=True):
        st.session_state.current_page = 'login'
        st.rerun()

    st.markdown("""
        <div class="security-features">
            <div class="feature-item">
                <span class="feature-icon">🔒</span>
                <span>Enterprise-grade security with advanced encryption</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">⚡</span>
                <span>Lightning-fast trade execution and real-time updates</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🛡️</span>
                <span>Protected by multi-factor authentication</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def logout():
    # Clear session state
    keys_to_clear = ['logged_in', 'user']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    # Clear browser storage
    st.query_params.clear()
    
    # Reset page to login
    st.session_state.current_page = 'login'

# function for login page
def login_page(db):
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #17171d 100%);
            background-size: 200% 200%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes glow {
            0% { box-shadow: 0 0 20px rgba(168, 85, 247, 0.1); }
            50% { box-shadow: 0 0 30px rgba(168, 85, 247, 0.2); }
            100% { box-shadow: 0 0 20px rgba(168, 85, 247, 0.1); }
        }
        
        .login-container {
            max-width: 450px;
            margin: 4rem auto;
            padding: 2.5rem;
            background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
            border-radius: 24px;
            box-shadow: 0 8px 32px rgba(168, 85, 247, 0.1);
            border: 1px solid rgba(168, 85, 247, 0.2);
            backdrop-filter: blur(10px);
            animation: glow 3s ease-in-out infinite;
        }
        
        .finch-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(90deg, #a855f7, #d946ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        
        .subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Form fields */
        .stTextInput input {
            background: rgba(23, 23, 30, 0.9);
            border: 1px solid rgba(168, 85, 247, 0.3);
            color: #f8fafc;
            border-radius: 12px;
            padding: 1rem;
            transition: all 0.3s ease;
            font-size: 1rem;
        }
        
        .stTextInput input:focus {
            border-color: #a855f7;
            box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
        }
        
        /* Submit button */
        .stButton button {
            background: linear-gradient(90deg, #7d1cc2, #ab23b3) !important;

            color: white !important;
            border: none !important;
            padding: 1rem !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(168, 85, 247, 0.3);
        }
        
        .divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 1.5rem 0;
            color: rgba(168, 85, 247, 0.5);
            font-size: 0.9rem;
        }
        
        .error-message {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #ef4444;
            padding: 1rem;
            border-radius: 12px;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="login-container">
            <div class="finch-title">Finch</div>
            <div class="subtitle">Welcome back, trader</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form('login_form'):
        email = st.text_input('Email', placeholder='Enter your email')
        password = st.text_input('Password', type='password', placeholder='Enter your password')
        submitted = st.form_submit_button('Sign In', use_container_width=True)

        if submitted:
            user_details = db.verify_user(email, password)
            if user_details:
                st.session_state.logged_in = True
                st.session_state.user = user_details
                st.session_state.current_page = 'trading'
                st.rerun()
            else:
                st.error('Invalid email or password')
    
    st.markdown('<div class="divider">New to Finch?</div>', unsafe_allow_html=True)
    
    if st.button('Create New Account', use_container_width=True):
        st.session_state.current_page = 'register'
        st.rerun()

    # Brief security message
    st.markdown("""
        <div style="
            text-align: center;
            margin-top: 2rem;
            padding: 1.5rem;
            background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
            border-radius: 16px;
            border: 1px solid rgba(168, 85, 247, 0.2);
        ">
            <div style="
                color: #a855f7;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
            ">
                <span>🔐</span>
                <span>Secure Trading Platform</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5;">
                Your security is our top priority. We use industry-leading encryption 
                to protect your data and investments.
            </div>
        </div>
    """, unsafe_allow_html=True)