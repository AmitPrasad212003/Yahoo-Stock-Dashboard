import streamlit as st
import yfinance as yf
import plotly.express as pe

# --- Futuristic UI Theme ---
st.markdown("""
    <style>
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .sidebar .sidebar-content {
            background: #2E2E2E;
        }
        .stButton>button {
            background: linear-gradient(to right, #06beb6, #48b1bf);
            border: none;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px;
        }
        .stTextInput>div>div>input {
            background-color: #444;
            color: white;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.title("🚀 Yahoo Stock Dashboard")
st.markdown("Analyze stock market trends in a futuristic interface.")

# --- Sidebar Layout ---
st.sidebar.title('📊 Stock Analysis Panel')
ticker_symbol = st.sidebar.text_input("Enter Ticker Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

if start_date and end_date:
    try:
        ticker = yf.Ticker(ticker_symbol)
        historical_data = ticker.history(start=start_date, end=end_date)

        if historical_data.empty:
            st.error("❌ No data found! Please check the ticker symbol or date range.")
        else:
            st.subheader(f'📈 {ticker_symbol} Stock Overview')

            # Fetch stock data
            stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

            # Debugging: Show available columns
            st.write("✅ Available columns:", stock_data.columns)

            # Choose column dynamically
            y_column = "Adj Close" if "Adj Close" in stock_data.columns else "Close"

            # --- Tabs for Better Organization ---
            price_tab, hist_tab, chart_tab = st.tabs(["📉 Price Summary", "📜 Historical Data", "📊 Charts"])

            with price_tab:
                st.subheader("💰 Price Summary")
                st.write(stock_data)

            with hist_tab:
                st.subheader("📜 Historical Data")
                st.write(historical_data)

            with chart_tab:
                st.subheader("📊 Interactive Chart")

                # Create a futuristic line chart
                line_chart = pe.line(
                    stock_data, 
                    x=stock_data.index, 
                    y=stock_data[y_column], 
                    title=f"{ticker_symbol} Stock Price"
                )

                # Add axis labels
                line_chart.update_xaxes(title="Date", color="white", showgrid=False)
                line_chart.update_yaxes(title="Stock Price (USD)", color="white", showgrid=False)
                line_chart.update_layout(plot_bgcolor="#1E1E1E", paper_bgcolor="#1E1E1E", font=dict(color="white"))

                # Display the chart
                st.plotly_chart(line_chart)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
