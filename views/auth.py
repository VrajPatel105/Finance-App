import streamlit as st

# Function to load Registration page
def register_page(db):
    # Custom CSS for the registration page
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, #0f172a, #1e293b);
            color: #e2e8f0;
        }
        
        .register-container {
            max-width: 500px;
            margin: 2rem auto;
            padding: 2rem;
            background: rgba(30, 41, 59, 0.8);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(59, 130, 246, 0.1);
        }
        
        .register-header {
            text-align: center;
            margin-bottom: 2rem;
            color: #e2e8f0;
        }
        
        /* Make form inputs more visually appealing */
        .stTextInput input {
            background-color: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #e2e8f0;
            border-radius: 8px;
            padding: 0.75rem;
            transition: all 0.3s;
        }
        
        .stTextInput input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }
        
        /* Style the registration button */
        .stButton button {
            width: 100%;
            padding: 0.75rem;
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%) !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s;
            margin-top: 0.5rem;
        }
        
        /* Style success and error messages */
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .success {
            background-color: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.2);
            color: #22c55e;
        }
        
        .error {
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }
        
        /* Add helpful tooltips */
        .tooltip {
            font-size: 0.85rem;
            color: #64748b;
            margin-top: 0.25rem;
        }
        
        /* Style for the divider */
        .divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 1rem 0;
            color: #64748b;
        }
        
        .divider::before,
        .divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid #64748b;
        }
        
        .divider:not(:empty)::before {
            margin-right: 1rem;
        }
        
        .divider:not(:empty)::after {
            margin-left: 1rem;
        }
        
        /* Style for the login button */
        .login-button {
            margin-top: 1rem;
        }
        
        .login-button button {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid #3b82f6 !important;
            color: #3b82f6 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create a container for the registration form
    st.markdown("""
        <div class="register-container">
            <div class="register-header">
                <h1>Create Your Account</h1>
                <p style="color: #64748b;">Join our trading community today!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Start the registration form with input validation
    with st.form('register_form'):
        # Get user's full name
        name = st.text_input(
            'Full Name',
            placeholder='Enter your full name',
            help='Please enter your full name as it appears on official documents'
        )

        # Get user's email address
        email = st.text_input(
            'Email Address',
            placeholder='your.email@example.com',
            help='We\'ll send a verification link to this email'
        )

        # Create columns for password fields to place them side by side
        col1, col2 = st.columns(2)
        
        with col1:
            # Get user's chosen password
            password = st.text_input(
                'Create Password',
                type='password',
                placeholder='••••••••',
                help='Use at least 8 characters with letters and numbers'
            )

        with col2:
            # Confirm the password
            confirm_password = st.text_input(
                'Confirm Password',
                type='password',
                placeholder='••••••••',
                help='Re-enter your password'
            )

        # Add the registration button
        submitted = st.form_submit_button('Create Account', use_container_width=True)

    # Handle form submission and validation
    if submitted:
        # Check if passwords match
        if password != confirm_password:
            st.error('🔐 Passwords don\'t match. Please try again.')
        
        # Ensure all required fields are filled
        elif not all([name, email, password]):
            st.error('📝 Please fill in all fields to complete registration.')
        
        # If all validations pass, attempt to create the account
        else:
            # Try to add the new user to the database
            user_id = db.add_user(name, email, password)
            
            if user_id:
                # Show success message and redirect to login
                st.success('🎉 Welcome aboard! Your account has been created successfully.')
                
                # Add a small delay for better UX
                import time
                time.sleep(1)
                
                # Redirect to login page
                st.session_state.current_page = 'login'
                st.rerun()
            else:
                # Show error if registration fails (usually due to duplicate email)
                st.error('📧 This email is already registered. Please try logging in or use a different email.')

    # Add divider
    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
    
    # Add login button with custom class
    st.markdown('<div class="login-button">', unsafe_allow_html=True)
    if st.button('Already have an account? Login', use_container_width=True):
        st.session_state.current_page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Add helpful tips at the bottom
    st.markdown("""
        <div class="tooltip">
            ℹ️ By registering, you agree to our Terms of Service and Privacy Policy.<br>
            🔒 We use industry-standard encryption to protect your data.<br>
            📱 After registration, we recommend enabling two-factor authentication.
        </div>
    """, unsafe_allow_html=True)


# Function to load the login page
def login_page(db):
    # Custom CSS for login page
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, #0f172a, #1e293b);
            color: #e2e8f0;
        }
        
        .login-container {
            max-width: 450px;
            margin: 2rem auto;
            padding: 2rem;
            background: rgba(30, 41, 59, 0.8);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(59, 130, 246, 0.1);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
            color: #e2e8f0;
        }
        
        /* Style for form inputs */
        .stTextInput input {
            background-color: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #e2e8f0;
            border-radius: 8px;
            padding: 0.75rem;
            transition: all 0.3s;
        }
        
        .stTextInput input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }
        
        /* Style for buttons */
        .stButton button {
            width: 100%;
            padding: 0.75rem;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s;
            margin-top: 0.5rem;
        }
        
        .login-form-submit {
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%) !important;
            color: white !important;
        }
        
        .register-button {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid #3b82f6 !important;
            color: #3b82f6 !important;
        }
        
        .divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 1rem 0;
            color: #64748b;
        }
        
        .divider::before,
        .divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid #64748b;
        }
        
        .divider:not(:empty)::before {
            margin-right: 1rem;
        }
        
        .divider:not(:empty)::after {
            margin-left: 1rem;
        }
        
        .stAlert {
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }
        </style>
    """, unsafe_allow_html=True)

    # Login container
    st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1>Finch</h1>
                <p style="color: #64748b;">Welcome back! Please login to your account.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Login form inside the container
    with st.form('login_form'):
        email = st.text_input('Email', placeholder='Enter your email')
        password = st.text_input('Password', type='password', placeholder='Enter your password')
        
        # Submit button with custom styling
        submitted = st.form_submit_button('Login', use_container_width=True)
        
        if submitted:
            user = db.verify_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.current_page = 'trading'
                st.rerun()
            else:
                st.error('Invalid email or password')
    
    # Divider
    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
    
    # Register button
    if st.button('Create New Account', use_container_width=True):
        st.session_state.current_page = 'register'
        st.rerun()


# Function to logout
def logout():
    st.session_state.logged_in = False
    st.session_state.current_page = 'login'
    st.session_state.user = None  # This will forget the user