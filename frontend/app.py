import streamlit as st
import requests
import json
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="🤖 Agentic Chatbot", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .ai-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None
if 'available_models' not in st.session_state:
    st.session_state.available_models = None

# Authentication functions
def login(username, password):
    """Login user and get auth token"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None

def register(username, email, password):
    """Register new user"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            st.success("Registration successful! Please login.")
            return True
        else:
            st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False

def get_available_models():
    """Fetch available models and roles"""
    try:
        response = requests.get(f"{API_BASE_URL}/chat/models")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching models: {str(e)}")
        return None

def send_message(message, model_name, model_provider, role, search_enabled, temperature, auth_token):
    """Send message to chatbot"""
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        payload = {
            "session_id": st.session_state.session_id,
            "message": message,
            "model_name": model_name,
            "model_provider": model_provider,
            "role": role,
            "search_enabled": search_enabled,
            "temperature": temperature
        }
        
        response = requests.post(f"{API_BASE_URL}/chat/", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None



# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Agentic Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent AI Agents with Web Search Capabilities</p>', unsafe_allow_html=True)
    
    # Authentication check
    if not st.session_state.auth_token:
        show_auth_page()
        return
    
    # Load available models if not cached
    if not st.session_state.available_models:
        with st.spinner("Loading available models..."):
            st.session_state.available_models = get_available_models()
    
    if not st.session_state.available_models:
        st.error("Failed to load available models. Please check your backend connection.")
        return
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("## 🛠️ Configuration")
        
        # Model Selection
        st.markdown("### 🤖 Model Settings")
        
        # Provider selection
        providers = ["gemini", "groq"]
        selected_provider = st.selectbox(
            "Select Provider:",
            providers,
            format_func=lambda x: x.title()
        )
        
        # Model selection based on provider
        if selected_provider == "gemini":
            available_models = st.session_state.available_models["gemini"]["models"]
            default_temp = st.session_state.available_models["gemini"]["temperature"]
        else:
            available_models = st.session_state.available_models["groq"]["models"]
            default_temp = st.session_state.available_models["groq"]["temperature"]
        
        selected_model = st.selectbox("Select Model:", available_models)
        
        # Role selection
        st.markdown("### 🎭 Agent Role")
        roles = st.session_state.available_models["roles"]
        role_options = {role["id"]: f"{role['name']} - {role['description']}" for role in roles}
        
        selected_role = st.selectbox(
            "Select Agent Role:",
            options=list(role_options.keys()),
            format_func=lambda x: role_options[x]
        )
        
        # Advanced settings
        st.markdown("### ⚙️ Advanced Settings")
        
        temperature = st.slider(
            "Temperature (Creativity):",
            min_value=0.0,
            max_value=2.0,
            value=default_temp,
            step=0.1,
            help="Higher values make output more creative but less focused"
        )
        
        search_enabled = st.checkbox(
            "🔍 Enable Web Search",
            value=True,
            help="Allow the agent to search the web for current information"
        )
        
        # Session management
        st.markdown("### 💬 Session")
        if st.button("🔄 New Session"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
        
        if st.button("🚪 Logout"):
            st.session_state.auth_token = None
            st.session_state.messages = []
            st.rerun()
        
        # Display current session info
        st.markdown(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat history
        st.markdown("## 💬 Chat History")
        
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 You:</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <strong>🤖 {message.get('agent_role', 'AI Assistant')}:</strong><br>
                        {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Message input
        st.markdown("## ✍️ Send Message")
        
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Your message:",
                height=100,
                placeholder="Ask me anything! I can search the web for current information..."
            )
            
            col_send, col_clear = st.columns([1, 1])
            with col_send:
                send_button = st.form_submit_button("🚀 Send Message", use_container_width=True)
            with col_clear:
                if st.form_submit_button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()
        
        # Handle message sending
        if send_button and user_input.strip():
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now()
            })
            
            # Show loading spinner
            with st.spinner("🤔 AI is thinking..."):
                # Send message to backend
                response = send_message(
                    user_input,
                    selected_model,
                    selected_provider,
                    selected_role,
                    search_enabled,
                    temperature,
                    st.session_state.auth_token
                )
                
                if response:
                    # Add AI response to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["ai_response"],
                        "agent_role": response.get("role", "AI Assistant"),
                        "model": response.get("model_name"),
                        "provider": response.get("model_provider"),
                        "search_used": response.get("search_enabled", False),
                        "timestamp": datetime.now()
                    })
            
            st.rerun()
    
    with col2:
        # Statistics and info panel
        st.markdown("## 📊 Session Stats")
        
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        ai_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.metric("Total Messages", total_messages)
        st.metric("Your Messages", user_messages)
        st.metric("AI Responses", ai_messages)
        
        # Current configuration
        st.markdown("## 🔧 Current Config")
        st.markdown(f"**Provider:** {selected_provider.title()}")
        st.markdown(f"**Model:** {selected_model}")
        st.markdown(f"**Role:** {[r['name'] for r in roles if r['id'] == selected_role][0]}")
        st.markdown(f"**Temperature:** {temperature}")
        st.markdown(f"**Web Search:** {'✅' if search_enabled else '❌'}")
        
        # Help section
        st.markdown("## ❓ Help")
        with st.expander("How to use"):
            st.markdown("""
            1. **Select a Provider**: Choose between Gemini or Groq
            2. **Pick a Model**: Different models have different capabilities
            3. **Choose a Role**: Each role specializes in different topics
            4. **Enable Web Search**: For current information and real-time data
            5. **Adjust Temperature**: Higher = more creative, Lower = more focused
            6. **Start Chatting**: Ask questions and get intelligent responses!
            """)
        
        with st.expander("Agent Roles"):
            for role in roles:
                st.markdown(f"**{role['name']}**: {role['description']}")

def show_auth_page():
    """Show authentication page"""
    st.markdown("## 🔐 Authentication Required")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### 👤 Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("🚀 Login", use_container_width=True):
                if username and password:
                    token = login(username, password)
                    if token:
                        st.session_state.auth_token = token
                        st.success("Login successful!")
                        st.rerun()
                else:
                    st.error("Please enter both username and password")
    
    with tab2:
        st.markdown("### 📝 Register")
        with st.form("register_form"):
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.form_submit_button("📝 Register", use_container_width=True):
                if reg_username and reg_email and reg_password and reg_confirm_password:
                    if reg_password == reg_confirm_password:
                        register(reg_username, reg_email, reg_password)
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")

if __name__ == "__main__":
    main()