"""
Streamlit Frontend for Piper Alpha Training Progress Tracking System.
Main application file with login/register and dashboard functionality.
"""

import streamlit as st
import requests
from datetime import datetime
import os
from typing import Optional, Dict, List

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Test API connection
try:
    _test_response = requests.get(f"{API_BASE_URL}/", timeout=2)
    _api_status = "✅ Connected" if _test_response.status_code == 200 else f"⚠️ Status {_test_response.status_code}"
except:
    _api_status = "❌ Not Connected"

# Page configuration
st.set_page_config(
    page_title="Piper Alpha Training System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a237e;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1a237e;
        color: white;
        font-weight: bold;
    }
    .session-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f5f5f5;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"


# ========== API Helper Functions ==========

def register_user(email: str, password: str, role: str, trainee_name: str) -> Dict:
    """Register a new user via API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/register",
            json={
                "email": email,
                "password": password,
                "role": role,
                "trainee_name": trainee_name
            }
        )
        if response.status_code == 201:
            return {"success": True, "data": response.json()}
        else:
            try:
                error_detail = response.json().get("detail", "Registration failed")
            except:
                error_detail = f"Registration failed (Status: {response.status_code}). Response: {response.text[:200]}"
            return {"success": False, "error": error_detail}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": f"Cannot connect to backend at {API_BASE_URL}. Is it running?"}
    except Exception as e:
        error_msg = str(e)
        # Don't show JSON parsing errors to end user
        if "Expecting value" in error_msg:
            error_msg = "Registration failed. Please try again."
        return {"success": False, "error": f"Error: {error_msg}"}


def login_user(email: str, password: str) -> Dict:
    """Login user and get JWT token."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={
                "email": email,
                "password": password
            }
        )
        if response.status_code == 200:
            token_data = response.json()
            # Get user details
            user_response = requests.get(
                f"{API_BASE_URL}/me",
                headers={"Authorization": f"Bearer {token_data['access_token']}"}
            )
            if user_response.status_code == 200:
                return {
                    "success": True,
                    "token": token_data["access_token"],
                    "user": user_response.json()
                }
        try:
            error_detail = response.json().get("detail", "Login failed")
        except:
            error_detail = f"Login failed (Status: {response.status_code})"
        return {"success": False, "error": error_detail}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": f"Cannot connect to backend at {API_BASE_URL}"}
    except Exception as e:
        error_msg = str(e)
        # Don't show JSON parsing errors to end user
        if "Expecting value" in error_msg:
            error_msg = "Login failed. Please check your credentials."
        return {"success": False, "error": f"Error: {error_msg}"}


def get_performance_data(email: str, token: str) -> Optional[List[Dict]]:
    """Get user's performance data."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/performance/{email}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            try:
                return response.json()
            except:
                return None
        return None
    except Exception as e:
        # Don't show JSON parsing errors to user
        if "Expecting value" not in str(e):
            st.error(f"Error fetching data: {str(e)}")
        return None


def download_report(session_id: int, token: str, filename: str):
    """Download PDF report for a session."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/download-report/{session_id}",
            headers={"Authorization": f"Bearer {token}"},
            stream=True
        )
        if response.status_code == 200:
            return response.content
        else:
            try:
                error_msg = response.json().get('detail', 'Unknown error')
            except:
                error_msg = f"Error (Status {response.status_code})"
            # Don't show JSON parsing errors
            if "Expecting value" not in error_msg:
                st.error(f"Error downloading report: {error_msg}")
            return None
    except Exception as e:
        # Don't show JSON parsing errors
        if "Expecting value" not in str(e):
            st.error(f"Error: {str(e)}")
        return None


# ========== Authentication Pages ==========

def show_login_page():
    """Display login/register page."""
    st.markdown('<div class="main-header">🎓 Piper Alpha Training System</div>', unsafe_allow_html=True)
    st.caption(f"Backend API: {API_BASE_URL} {_api_status}")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # Login Tab
    with tab1:
        st.markdown("### Login to Your Account")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    with st.spinner("Logging in..."):
                        result = login_user(email, password)
                        
                        if result["success"]:
                            st.session_state.token = result["token"]
                            st.session_state.user = result["user"]
                            st.session_state.page = "dashboard"
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")
    
    # Register Tab
    with tab2:
        st.markdown("### Create New Account")
        
        with st.form("register_form"):
            reg_email = st.text_input("Email", placeholder="your.email@example.com", key="reg_email")
            reg_name = st.text_input("Full Name", placeholder="John Doe", key="reg_name")
            reg_role = st.selectbox("Role", ["Trainee", "Admin"], key="reg_role")
            reg_password = st.text_input("Password (min 8 characters)", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            reg_submit = st.form_submit_button("Register", use_container_width=True)
            
            if reg_submit:
                if not all([reg_email, reg_name, reg_password, reg_confirm]):
                    st.error("Please fill in all fields")
                elif len(reg_password) < 8:
                    st.error("Password must be at least 8 characters")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match")
                else:
                    with st.spinner("Creating account..."):
                        result = register_user(reg_email, reg_password, reg_role, reg_name)
                        
                        if result["success"]:
                            st.success("✅ Registration successful! Please login.")
                        else:
                            st.error(f"❌ {result['error']}")


# ========== Dashboard Page ==========

def show_dashboard():
    """Display user dashboard with performance sessions."""
    user = st.session_state.user
    token = st.session_state.token
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### Welcome, {user['trainee_name']}!")
        st.write(f"**Role:** {user['role']}")
        st.write(f"**Email:** {user['email']}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
    
    # Main content
    st.markdown(f'<div class="main-header">📊 Training Progress Dashboard</div>', unsafe_allow_html=True)
    
    # Fetch performance data
    with st.spinner("Loading your training sessions..."):
        sessions = get_performance_data(user["email"], token)
    
    if sessions is None:
        st.error("Failed to load performance data")
        return
    
    if len(sessions) == 0:
        st.info("📝 No training sessions found. Complete chapters in the Unity game to see your progress here.")
        return
    
    # Display sessions
    st.markdown(f"### Your Training Sessions ({len(sessions)} total)")
    
    for session in sessions:
        session_id = session["id"]
        timestamp = datetime.fromisoformat(session["session_timestamp"].replace('Z', '+00:00'))
        chapter_data = session["chapter_data"]
        
        # Calculate stats
        completed = sum(1 for ch in chapter_data if ch["status"] == "Completed")
        total = len(chapter_data)
        scores = [int(ch["score"]) for ch in chapter_data if ch["score"] != "NA"]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Display session card
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.write(f"**📅 {timestamp.strftime('%B %d, %Y at %I:%M %p')}**")
        
        with col2:
            st.write(f"**Completed:** {completed}/{total} chapters")
        
        with col3:
            st.write(f"**Avg Score:** {avg_score:.1f}/10")
        
        with col4:
            # Download button - only fetch when clicked
            if st.button("📥", key=f"download_btn_{session_id}", help="Download PDF Report"):
                with st.spinner("Generating PDF..."):
                    pdf_data = download_report(session_id, token, f"report_{session_id}.pdf")
                    if pdf_data:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_data,
                            file_name=f"PiperAlpha_Report_{user['trainee_name'].replace(' ', '_')}_{timestamp.strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            key=f"download_{session_id}"
                        )
        
        # Expandable details
        with st.expander("View Chapter Details"):
            for chapter in chapter_data:
                status_emoji = "✅" if chapter["status"] == "Completed" else "⏳" if chapter["status"] == "Pending" else "❌"
                st.write(f"{status_emoji} **{chapter['chapter']}** - Score: {chapter['score']}/10 ({chapter['status']})")
        
        st.markdown("---")


# ========== Main App Logic ==========

def main():
    """Main application entry point."""
    
    # Check authentication
    if st.session_state.token is None:
        show_login_page()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()

