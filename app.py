
import streamlit as st
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent))

# Custom modules
from config.config import Config
from src.ui import sidebar, dashboard, analysis, charts, insights
from src.database.supabase_client import SupabaseClient
from src.integrations.topstep_client import TopStepClient
from src.integrations.databento_client import DatabentoClient
from src.analysis.nlp_processor import NLPProcessor
from src.analysis.trade_analytics import TradeAnalytics
from src.analysis.predictive_engine_enhanced import EnhancedPredictiveEngine
from src.utils.sample_data_generator import SampleDataGenerator

# Load environment variables
load_dotenv()

# --- Initialize Clients --- #
@st.cache_resource
def init_clients():
    supabase_client = SupabaseClient(Config.SUPABASE_URL, Config.SUPABASE_KEY) if Config.is_supabase_configured() else None
    topstep_client = TopStepClient(Config.TOPSTEP_API_KEY) if Config.is_topstep_configured() else None
    databento_client = DatabentoClient(Config.DATABENTO_API_KEY) if Config.is_databento_configured() else None
    nlp_processor = NLPProcessor(Config.OPENAI_API_KEY, Config.OPENAI_MODEL) if Config.is_openai_configured() else None
    return supabase_client, topstep_client, databento_client, nlp_processor

supabase_client, topstep_client, databento_client, nlp_processor = init_clients()

# --- Data Loading and Processing --- #
@st.cache_data(ttl=3600) # Cache data for 1 hour
def load_data(use_sample_data: bool = False):
    trades = []
    journals = []
    market_data = {}

    if use_sample_data:
        st.info("Loading sample data...")
        generator = SampleDataGenerator()
        trades = generator.generate_trades(num_trades=100)
        journals = generator.generate_journals(trades)
        
        # Load sample market data for MES
        sample_market_data_path = "./data/sample_market_data_MES.csv"
        if os.path.exists(sample_market_data_path):
            market_data["MES"] = pd.read_csv(sample_market_data_path)
            market_data["MES"]["timestamp"] = pd.to_datetime(market_data["MES"]["timestamp"])
        else:
            st.warning(f"Sample market data not found at {sample_market_data_path}. Please run sample_data_generator.py.")

    else:
        if supabase_client:
            try:
                trades = supabase_client.fetch_trades()
                journals = supabase_client.fetch_journals()
                st.success("Data fetched from Supabase.")
            except Exception as e:
                st.error(f"Error fetching data from Supabase: {e}")
        else:
            st.warning("Supabase client not configured. Cannot fetch live data.")

        # Fetch market data for relevant symbols (e.g., from trades)
        if databento_client and trades:
            unique_symbols = list(set([trade["symbol"] for trade in trades]))
            for symbol in unique_symbols:
                try:
                    # Assuming get_candlestick_data can fetch historical data
                    # For simplicity, fetching for a fixed period for now
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=30)
                    market_data[symbol] = databento_client.get_candlestick_data(symbol, start_date, end_date)
                except Exception as e:
                    st.error(f"Error fetching market data for {symbol} from Databento: {e}")

    return trades, journals, market_data

# --- Main Application --- #
def main():
    st.set_page_config(layout="wide", page_title="Phase 2 AI Analysis App", page_icon="📈")

    st.title("📈 Phase 2 AI Analysis & Enhancement App")

    # Sidebar for navigation and configuration status
    selected_page = sidebar.render_sidebar(Config)

    # Validate configuration (using the Config class from config.py)
    missing_config = Config.validate()
    if missing_config:
        st.error(f"⚠️ Missing required configuration: {', '.join(missing_config)}")
        st.info("Please set up your `.env` file with the required API keys. See `.env.example` for reference.")
        # st.stop() # Do not stop, allow sample data to be used

    # Display configuration summary in expander
    with st.expander("🔧 Configuration Status"):
        config_summary = Config.get_summary()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Environment", config_summary["app_env"])
            st.metric("Supabase", "✅" if config_summary["supabase_configured"] else "❌")
        with col2:
            st.metric("OpenAI Model", config_summary["openai_model"])
            st.metric("TopStep API", "✅" if config_summary["topstep_configured"] else "❌")
        with col3:
            st.metric("Discord Bot", "✅" if config_summary["discord_enabled"] else "❌")
            st.metric("Databento API", "✅" if config_summary["databento_configured"] else "❌")
    
    st.divider()

    # Check if any API keys are configured
    is_any_api_configured = (
        Config.is_supabase_configured() or
        Config.is_topstep_configured() or
        Config.is_databento_configured() or
        Config.is_openai_configured()
    )

    use_sample_data = st.checkbox("Use Sample Data (if no live data configured or for demo)", value=not is_any_api_configured)

    trades, journals, market_data = load_data(use_sample_data)

    # Initialize analytics and predictive engine
    trade_analytics = TradeAnalytics(trades)
    # Pass MES market data for now, assuming it's the primary symbol for analysis
    predictive_engine = EnhancedPredictiveEngine(trades, journals, market_data.get("MES")) 

    # Page Routing
    if selected_page == "Dashboard":
        dashboard.render_page(trade_analytics, trades, journals)
    elif selected_page == "Trade Analysis":
        analysis.render_page(trade_analytics, trades, journals)
    elif selected_page == "Interactive Charts":
        charts.render_page(trades, journals, market_data)
    elif selected_page == "AI Insights":
        insights.render_page(predictive_engine, nlp_processor, trades, journals, market_data)

if __name__ == "__main__":
    main()

