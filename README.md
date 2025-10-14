# Phase 2 AI Analysis and Enhancement App

This repository contains the code for the Phase 2 AI Analysis and Enhancement App, a web-based tool built with Streamlit. It integrates trading journal data from your Phase 1 PWA, trade history from TopStep, and market data from Databento to provide advanced AI-powered insights, prescriptive recommendations, and predictive analytics for futures trading.

## Features

*   **Data Integration:** Seamlessly syncs with Supabase for journal and trade data, integrates with TopStep API for trade history, and Databento for real-time/historical market data.
*   **NLP & Auto-Tagging:** Uses OpenAI GPT-4o-mini to analyze journal entries, extract emotional states, and auto-generate relevant tags.
*   **Advanced Trade Analytics:** Calculates key performance indicators like MFE/MAE, R:R ratios, hold times, win/loss streaks, expectancy, profit factor, and prop firm compliance metrics.
*   **Interactive Charting:** MT4/MT5-style candlestick charts with Plotly, overlaying trade entries/exits and journal annotations.
*   **Prescriptive Analysis:** Provides real-time, actionable recommendations based on identified trading patterns, emotional states, and market conditions.
*   **Predictive Analytics:** Leverages machine learning models (e.g., clustering, time-series) to forecast trade outcomes, identify optimal setups, and discover hidden edges.
*   **User Authentication & Subscriptions:** Secure user management via Supabase Auth and integrated Stripe for future subscription models.

## Project Structure

```
phase2-ai-analysis-app/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── README.md                   # Project README and deployment guide
├── config/
│   └── config.py               # Centralized application configuration
├── src/
│   ├── analysis/
│   │   ├── nlp_processor.py    # NLP for journal tagging and sentiment
│   │   ├── predictive_engine.py # Core AI for prescriptive/predictive analysis
│   │   └── trade_analytics.py  # Mathematical models for trade analysis
│   ├── auth/
│   │   └── auth_manager.py     # User authentication and subscription management
│   ├── database/
│   │   └── supabase_client.py  # Supabase database client
│   ├── integrations/
│   │   ├── databento_client.py # Databento market data client
│   │   └── topstep_client.py   # TopStep API client
│   └── ui/
│       ├── analysis.py         # UI for trade analysis page
│       ├── charts.py           # UI for interactive charts page
│       ├── dashboard.py        # UI for main dashboard page
│       ├── insights.py         # UI for AI insights and predictions page
│       └── sidebar.py          # UI for application sidebar and navigation
├── data/                       # Placeholder for sample data or local storage
├── docs/                       # Documentation (e.g., database schema)
│   └── database_schema.sql     # Supabase SQL schema setup
├── tests/                      # Unit and integration tests
└── utils/                      # Utility scripts
```

## Setup and Local Development

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd phase2-ai-analysis-app
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project based on `.env.example`. Fill in your API keys and URLs:
    ```ini
    # Supabase Configuration
    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_anon_key

    # OpenAI Configuration
    OPENAI_API_KEY=your_openai_api_key

    # TopStep API Configuration
    TOPSTEP_API_KEY=your_topstep_api_key
    TOPSTEP_API_URL=https://api.topstepx.com

    # Databento Configuration
    DATABENTO_API_KEY=your_databento_api_key

    # Stripe Configuration (for future subscription features)
    STRIPE_API_KEY=your_stripe_api_key
    STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

    # OneSignal Configuration (for push notifications)
    ONESIGNAL_APP_ID=your_onesignal_app_id
    ONESIGNAL_REST_API_KEY=your_onesignal_rest_api_key

    # Optional: AssemblyAI Configuration (for voice transcription)
    # ASSEMBLYAI_API_KEY=your_assemblyai_api_key

    # Optional: Discord Bot Configuration
    # DISCORD_BOT_TOKEN=your_discord_bot_token
    # DISCORD_CHANNEL_ID=your_discord_channel_id

    # Application Configuration
    APP_ENV=development
    DEBUG_MODE=True
    ```

4.  **Set up Supabase Database:**
    Go to your Supabase project dashboard, navigate to the SQL Editor, and run the commands in `docs/database_schema.sql` to create the necessary tables and Row Level Security (RLS) policies.

5.  **Run the Streamlit application locally:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser, usually at `http://localhost:8501`.

## Deployment to Vercel

This Streamlit application can be easily deployed to Vercel. Follow these steps:

1.  **Create a Vercel Account:** If you don't have one, sign up at [vercel.com](https://vercel.com/).

2.  **Connect to Git Repository:** Push your project to a Git repository (GitHub, GitLab, or Bitbucket). Vercel integrates directly with these services.

3.  **Import Your Project:**
    *   Go to your Vercel Dashboard.
    *   Click 

`Add New Project`.
    *   Select your Git repository and click `Import`.

4.  **Configure Project Settings:**
    *   **Framework Preset:** Select `Other`.
    *   **Build Command:** `pip install -r requirements.txt && python -c 


```python -c "import streamlit.web.cli as stcli; stcli.main_run_func('app.py', 'streamlit run')"```
    *   **Output Directory:** Leave empty.
    *   **Development Command:** `streamlit run app.py`

5.  **Environment Variables:**
    *   Go to `Settings` -> `Environment Variables` in your Vercel project dashboard.
    *   Add all the variables from your `.env` file (e.g., `SUPABASE_URL`, `OPENAI_API_KEY`, `TOPSTEP_API_KEY`, `DATABENTO_API_KEY`, etc.). Ensure these are set correctly for your production environment.

6.  **Deploy:** Click `Deploy`. Vercel will build and deploy your Streamlit application. Once deployed, you will get a public URL for your app.

## Running the Discord Bot (Optional)

If you choose to enable the Discord bot, you will need to run it as a separate process, likely on a server or a persistent cloud instance (e.g., a small EC2 instance, Google Cloud Run, or a dedicated bot hosting service). It is not typically deployed directly to Vercel as Vercel is optimized for serverless web applications.

1.  **Install `discord.py`:**
    ```bash
    pip install discord.py
    ```
2.  **Create `discord_bot.py`:**
    (This file is not included in the current repository structure but would contain your bot logic).
3.  **Set `DISCORD_BOT_TOKEN`:** Ensure your `.env` file (or environment variables for your bot hosting) has `DISCORD_BOT_TOKEN` set.
4.  **Run the bot:**
    ```bash
    python discord_bot.py
    ```

## Testing with Sample Data

To test the application without connecting to live APIs, you can:

1.  **Populate Supabase with Sample Data:** Use the commented-out `INSERT` statements in `docs/database_schema.sql` to add sample users, journals, and trades.
2.  **Mock API Responses:** For more comprehensive testing, you can create mock versions of `topstep_client.py` and `databento_client.py` that return static sample data instead of making actual API calls.

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

