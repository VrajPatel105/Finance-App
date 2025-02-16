import streamlit as st
from database.connection import get_database
import hashlib
from datetime import datetime
import requests

class LocationTracker:
    @staticmethod
    def get_location():
        """Get user's location using IP-API (free service)"""
        try:
            response = requests.get('http://ip-api.com/json/')
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return {
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'country': data.get('country', 'Unknown'),
                        'timezone': data.get('timezone', 'UTC')
                    }
            return None
        except Exception as e:
            print(f"Error getting location: {e}")
            return None


def account_page():
    # Get user's location on page load
    if 'user_location' not in st.session_state:
        st.session_state.user_location = LocationTracker.get_location()
    
    st.markdown("""
    <style>
        /* Main containers */
        [data-testid="stVerticalBlock"] .account-container {
            background: linear-gradient(145deg, rgba(17, 17, 23, 0.95), rgba(28, 28, 35, 0.95));
            border-radius: 20px;
            padding: 2.5rem;
            margin: 1.5rem 0;
            border: 1px solid rgba(168, 85, 247, 0.2);
            box-shadow: 0 8px 32px rgba(168, 85, 247, 0.1);
            backdrop-filter: blur(10px);
        }
        
        /* Tabs styling */
        [data-testid="stVerticalBlock"] [data-baseweb="tab-list"] {
            background-color: transparent !important;
            padding: 0 !important;
            border: none !important;
        }

        [data-testid="stVerticalBlock"] [data-baseweb="tab"] {
            background-color: transparent !important;
            border: none !important;
            color: #94A3B8 !important;
            font-size: 1.1rem !important;
            padding: 0 1.5rem !important;
            margin-right: 1rem !important;
            position: relative !important;
        }

        [data-testid="stVerticalBlock"] [data-baseweb="tab"]::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            height: 2px;
            background: transparent;
            transition: all 0.3s ease;
        }

        [data-testid="stVerticalBlock"] [data-baseweb="tab"][aria-selected="true"] {
            color: #A855F7 !important;
        }

        [data-testid="stVerticalBlock"] [data-baseweb="tab"][aria-selected="true"]::after {
            background: linear-gradient(90deg, #A855F7, #D946EF);
        }
        
        /* Form fields */
        .account-container .stTextInput input {
            background: rgba(17, 17, 23, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 8px;
            color: #E2E8F0;
            padding: 0.8rem;
            height: auto;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .account-container .stTextInput input:focus {
            border-color: #A855F7;
            box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
        }
        
        .account-container .stSelectbox [data-baseweb="select"] {
            background: rgba(17, 17, 23, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 8px;
        }
        
        /* Buttons */
        .account-container .stButton button {
            background: linear-gradient(90deg, #A855F7, #D946EF);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .account-container .stButton button:hover {
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
            transform: translateY(-2px);
        }
        
        /* Alerts */
        .account-container .element-container .stAlert {
            background: rgba(17, 17, 23, 0.9);
            border: 1px solid;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .account-container .element-container .stAlert.success {
            border-color: rgba(72, 187, 120, 0.3);
            color: #48BB78;
        }
        
        .account-container .element-container .stAlert.error {
            border-color: rgba(245, 101, 101, 0.3);
            color: #F56565;
        }
        
        /* Section headers */
        .section-header {
            color: #A855F7;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 1.5rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(168, 85, 247, 0.2);
        }

        /* Profile stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1.5rem 0;
        }

        .stat-card {
            background: rgba(17, 17, 23, 0.6);
            border: 1px solid rgba(168, 85, 247, 0.2);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #A855F7;
            margin-bottom: 0.3rem;
        }

        .stat-label {
            color: #94A3B8;
            font-size: 0.9rem;
        }

        /* Activity list */
        .activity-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.8rem;
            border-bottom: 1px solid rgba(168, 85, 247, 0.1);
        }

        .activity-icon {
            background: rgba(168, 85, 247, 0.1);
            color: #A855F7;
            padding: 0.5rem;
            border-radius: 8px;
        }

        .activity-details {
            flex-grow: 1;
        }

        .activity-time {
            color: #94A3B8;
            font-size: 0.8rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Account Settings")
    
    # Get database connection
    db = get_database()
    
    # Create tabs with new design
    tabs = st.tabs([
        "📝 Profile", "🔒 Security"
    ])
    
    with tabs[0]:
        st.markdown('<div class="account-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Profile Information</div>', unsafe_allow_html=True)
        
        # Get current user info
        current_name = st.session_state.user.get('name', '')
        current_email = st.session_state.user.get('email', '')
        
        # Profile form
        with st.form("profile_form"):
            new_name = st.text_input("Name", value=current_name)
            new_email = st.text_input("Email", value=current_email)
            
            col1, col2 = st.columns(2)
            with col1:
                trading_experience = st.selectbox(
                    "Trading Experience",
                    ["Beginner", "Intermediate", "Advanced", "Professional"]
                )
            with col2:
                preferred_market = st.selectbox(
                    "Preferred Market",
                    ["Stocks", "Crypto", "Both"]
                )

            # Add phone number and timezone
            col3, col4 = st.columns(2)
            with col3:
                phone = st.text_input("Phone Number (Optional)")
            with col4:
                timezone = st.selectbox(
                    "Timezone",
                    ["UTC", "EST", "PST", "GMT", "IST"]
                )
            
            if st.form_submit_button("Update Profile"):
                user_id = st.session_state.user['id']
                db.change_email(user_id, new_email)
                st.success("Profile updated successfully!")

        # Add trading statistics
        st.markdown('<div class="section-header">Trading Statistics</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">$124,392</div>
                <div class="stat-label">Total Trading Volume</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">47</div>
                <div class="stat-label">Successful Trades</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">68.5%</div>
                <div class="stat-label">Win Rate</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Add recent activity
        st.markdown('<div class="section-header">Recent Activity</div>', unsafe_allow_html=True)
        
        activities = [
            ("💰 Trade", "Bought 10 shares of AAPL", "2 hours ago"),
            ("📊 Portfolio", "Updated investment strategy", "1 day ago"),
            ("🔒 Security", "Changed password", "3 days ago"),
            ("💳 Account", "Updated profile information", "1 week ago")
        ]

        for icon, action, time in activities:
            st.markdown(f"""
            <div class="activity-item">
                <span class="activity-icon">{icon}</span>
                <div class="activity-details">
                    <div>{action}</div>
                    <div class="activity-time">{time}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<div class="account-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Security Settings</div>', unsafe_allow_html=True)
        
        with st.form("security_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            submit_button = st.form_submit_button("Update Password")
            
            if submit_button:
                user_id = st.session_state.user['id']
                stored_password = db.get_password(user_id)
                entered_password = hashlib.sha256(current_password.encode()).hexdigest()
                
                if new_password != confirm_password:
                    st.error("New passwords don't match!")
                elif not current_password:
                    st.error("Please enter your current password!")
                elif entered_password != stored_password:
                    st.error('Your current password does not match!')
                else:
                    hashed_new = hashlib.sha256(new_password.encode()).hexdigest()
                    db.change_password(user_id, hashed_new)
                    st.success("Password updated successfully!")

        # Display location information
        st.markdown('<div class="section-header">Location Information</div>', unsafe_allow_html=True)
        
        # Current Location
        if st.session_state.user_location:
            loc = st.session_state.user_location
            # Log the location if it's new
            db.log_location(st.session_state.user['id'], loc)
            
            st.markdown(f"""
            <div style="background: rgba(17, 17, 23, 0.6); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <div style="color: #A855F7; font-size: 1.1rem; margin-bottom: 0.8rem;">Current Location</div>
                <div style="color: #E2E8F0; font-size: 1.2rem; margin-bottom: 0.5rem;">📍 {loc['city']}, {loc['region']}, {loc['country']}</div>
                <div style="color: #94A3B8; font-size: 0.9rem;">Timezone: {loc['timezone']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Location History
        location_history = db.get_location_history(st.session_state.user['id'])
        if location_history:
            st.markdown("""
            <div style="color: #A855F7; font-size: 1.1rem; margin: 1.5rem 0 1rem 0;">Recent Login Locations</div>
            """, unsafe_allow_html=True)
            
            for loc in location_history:
                city, region, country, timezone, device, timestamp = loc
                st.markdown(f"""
                <div class="activity-item">
                    <span class="activity-icon">🌍</span>
                    <div class="activity-details">
                        <div style="color: #E2E8F0;">{city}, {region}, {country}</div>
                        <div class="activity-time">{timestamp}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)