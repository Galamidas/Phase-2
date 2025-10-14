import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import databento as db
import pandas as pd
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Galamidas Phase 2",
    page_icon="⭐",
    layout="wide"
)

# --- Environment and API Key Management ---
# Load environment variables from .env file if it exists
load_dotenv()

# Use Streamlit secrets for deployment
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    databento_api_key = st.secrets["DATABENTO_API_KEY"]
except FileNotFoundError:
    # Fallback for local development using .env file
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    databento_api_key = os.getenv("DATABENTO_API_KEY")

# --- Initialization of Clients ---
@st.cache_resource
def init_supabase_client():
    """Initializes and returns the Supabase client."""
    if supabase_url and supabase_key:
        return create_client(supabase_url, supabase_key)
    return None

@st.cache_resource
def init_databento_client():
    """Initializes and returns the Databento client."""
    if databento_api_key:
        return db.Historical(databento_api_key)
    return None

supabase = init_supabase_client()
db_client = init_databento_client()

# --- Authentication Functions ---
def sign_up(email, password):
    """Signs up a new user."""
    if not supabase:
        st.error("Supabase client is not initialized. Check your API keys.")
        return None, "Supabase client not initialized."
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        st.success("Sign-up successful! Please check your email to verify your account.")
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    """Signs in an existing user."""
    if not supabase:
        st.error("Supabase client is not initialized. Check your API keys.")
        return None, "Supabase client not initialized."
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state['user'] = res.user
        st.success("Signed in successfully!")
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_out():
    """Signs out the current user."""
    if 'user' in st.session_state:
        del st.session_state['user']
    st.success("You have been signed out.")

# --- Main Application UI ---
st.title("Welcome to Galamidas - Phase 2")

# Check if user is logged in
if 'user' not in st.session_state:
    st.sidebar.header("User Authentication")
    auth_tab, about_tab = st.sidebar.tabs(["Authentication", "About"])

    with about_tab:
        st.info("This is the authentication portal for the Galamidas application.")

    with auth_tab:
        auth_form_choice = st.radio("Choose action:", ["Sign In", "Sign Up"])

        with st.form(key=f"{auth_form_choice.lower().replace(' ', '_')}_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label=auth_form_choice)

            if submit_button:
                if auth_form_choice == "Sign Up":
                    user, error = sign_up(email, password)
                    if error:
                        st.error(f"Sign-up failed: {error}")
                else:
                    user, error = sign_in(email, password)
                    if error:
                        st.error(f"Sign-in failed: {error}")
                    else:
                        st.rerun()

else:
    # --- Logged-in User View ---
    st.sidebar.header(f"Welcome, {st.session_state['user'].email}")
    st.sidebar.button("Sign Out", on_click=sign_out)

    st.header("Dashboard")
    st.write("You are now logged in and can access the application's features.")

    # Example: Fetching data from Databento
    if db_client:
        st.subheader("Databento Data Example")
        if st.button("Fetch Sample Data"):
            try:
                with st.spinner("Fetching data from Databento..."):
                    data = db_client.timeseries.get_range(
                        dataset="GLBX.MDP3",
                        symbols="ES.c.0",
                        schema="ohlcv-1m",
                        start="2024-01-01T00:00",
                        end="2024-01-02T00:00"
                    )
                    df = data.to_df()
                    st.success("Successfully fetched data!")
                    st.dataframe(df)
            except Exception as e:
                st.error(f"Failed to fetch data from Databento: {e}")
    else:
        st.warning("Databento client is not initialized. Please check your API key.")

