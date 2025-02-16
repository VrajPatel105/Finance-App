import streamlit as st
from database.connection import get_database
import hashlib

def account_page():
    st.markdown("""
    <style>
        .account-container {
            background: linear-gradient(145deg, rgba(32, 32, 40, 0.9), rgba(23, 23, 30, 0.9));
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid rgba(168, 85, 247, 0.2);
        }
        
        .section-title {
            color: #A855F7;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .info-card {
            background: rgba(23, 23, 30, 0.6);
            border: 1px solid rgba(168, 85, 247, 0.2);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .custom-field {
            background: rgba(23, 23, 30, 0.8);
            border: 1px solid rgba(168, 85, 247, 0.3);
            border-radius: 8px;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #E2E8F0;
        }
        
        .stat-label {
            color: #94A3B8;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Account Settings")
    
    # Get database connection
    db = get_database()
    
    # Create tabs for different sections
    profile_tab, security_tab, preferences_tab, stats_tab = st.tabs([
        "📝 Profile   ", "🔒 Security   ", "⚙️ Preferences   ", "📊 Statistics   "
    ])
    
    with profile_tab:
        st.markdown('<div class="account-container">', unsafe_allow_html=True)
        st.subheader("Profile Information")
        
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
            
            if st.form_submit_button("Update Profile"):
                
                user_id = st.session_state.user['id']
                db.change_email(user_id, new_email)

                st.success("Profile updated successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with security_tab:
        st.markdown('<div class="account-container">', unsafe_allow_html=True)
        st.subheader("Security Settings")
        
        with st.form("security_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password"):
                if new_password != confirm_password:
                    st.error("New passwords don't match!")
                elif not current_password:
                    st.error("Please enter your current password!")
                else:
                    # Hash passwords and verify
                    hashed_current = hashlib.sha256(current_password.encode()).hexdigest()
                    # Add password update logic here
                    st.success("Password updated successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with preferences_tab:
        st.markdown('<div class="account-container">', unsafe_allow_html=True)
        st.subheader("App Preferences")
        
        # Theme preference
        theme = st.selectbox(
            "Theme",
            ["Dark (Default)", "Extra Dark", "High Contrast"]
        )
        
        # Notification settings
        st.markdown("### Notifications")
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Price Alerts", value=True)
            st.checkbox("Portfolio Updates", value=True)
            st.checkbox("Market News", value=True)
        with col2:
            st.checkbox("Trade Confirmations", value=True)
            st.checkbox("Security Alerts", value=True)
            st.checkbox("Weekly Reports", value=True)
        
        if st.button("Save Preferences"):
            st.success("Preferences saved successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with stats_tab:
        st.markdown('<div class="account-container">', unsafe_allow_html=True)
        st.subheader("Account Statistics")
        
        # Account stats in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="info-card">
                <div class="stat-label">Account Age</div>
                <div class="stat-value">6 months</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="info-card">
                <div class="stat-label">Total Trades</div>
                <div class="stat-value">142</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="info-card">
                <div class="stat-label">Success Rate</div>
                <div class="stat-value">67.8%</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Add trading history or other stats
        st.markdown("### Recent Activity")
        activity_data = [
            "Password changed - 2 days ago",
            "Profile updated - 1 week ago",
            "Logged in from new device - 1 week ago",
            "Email verified - 2 weeks ago"
        ]
        
        for activity in activity_data:
            st.markdown(f"• {activity}")
        
        st.markdown('</div>', unsafe_allow_html=True)