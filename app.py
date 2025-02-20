import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI
st.title("📊 Stock Sentiment Analyzer")
st.subheader("Analyze if a stock is a BUY, SELL, or HOLD based on financial data.")

# User input for stock symbol
stock_name = st.text_input("Enter stock symbol (e.g., TCS, RELIANCE, INFY):", "").upper()

# Function to scrape financial data
def scrape_screener(stock_name):
    """Scrapes financial data of a given stock from Screener.in"""
    url = f"https://www.screener.in/company/{stock_name}/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"Error": f"Failed to fetch data for {stock_name}. Check stock symbol."}

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        company_name = extract_company_name(soup)
        market_cap = extract_value(soup, 'Market Cap')
        current_price = extract_value(soup, 'Current Price')
        high_low = extract_value(soup, 'High / Low')
        stock_pe = extract_value(soup, 'Stock P/E')
        dividend_yield = extract_value(soup, 'Dividend Yield')
        roce = extract_value(soup, 'ROCE')
        roe = extract_value(soup, 'ROE')

        # Perform Sentiment Analysis
        sentiment = get_sentiment(stock_pe, roce, roe, current_price, high_low, dividend_yield)

        return {
            'Company Name': company_name,
            'Market Cap': market_cap,
            'Current Price': current_price,
            'High / Low': high_low,
            'Stock P/E': stock_pe,
            'Dividend Yield': dividend_yield,
            'ROCE': roce,
            'ROE': roe,
            'Recommendation': sentiment
        }

    except Exception as e:
        return {"Error": f"Parsing error: {e}"}

def extract_company_name(soup):
    """Extracts the company name from the page."""
    company_name_tag = soup.find('h1', class_="company-name") or soup.find('h1', class_='margin-0')
    return company_name_tag.text.strip() if company_name_tag else 'N/A'

def extract_value(soup, label):
    """Extracts financial values based on the label."""
    try:
        label_tag = soup.find(string=lambda text: text and label in text)
        if label_tag:
            parent = label_tag.parent
            value_tag = parent.find_next(class_='number')
            return value_tag.text.strip() if value_tag else 'N/A'
        return 'N/A'
    except Exception:
        return 'N/A'

def get_sentiment(stock_pe, roce, roe, current_price, high_low, dividend_yield):
    """Performs basic sentiment analysis to decide Buy, Hold, or Sell"""
    try:
        pe_ratio = float(stock_pe) if stock_pe.replace('.', '', 1).isdigit() else None
        roce_value = float(roce.replace('%', '')) if roce.replace('%', '').replace('.', '', 1).isdigit() else None
        roe_value = float(roe.replace('%', '')) if roe.replace('%', '').replace('.', '', 1).isdigit() else None
        div_yield = float(dividend_yield.replace('%', '')) if dividend_yield.replace('%', '').replace('.', '', 1).isdigit() else None

        # Extract high and low values from High/Low string
        if "/" in high_low:
            low, high = map(lambda x: float(x.strip()), high_low.split('/'))
            price_ratio = (float(current_price) - low) / (high - low)
        else:
            price_ratio = None

        # Decision Logic
        if pe_ratio and pe_ratio < 20 and roce_value and roce_value > 15 and roe_value and roe_value > 15:
            return "✅ BUY 📈 (Good Fundamentals)"
        elif price_ratio and price_ratio > 0.8:
            return "⏳ WAIT (Too Expensive)"
        elif price_ratio and price_ratio < 0.2:
            return "📉 BUY (Undervalued)"
        elif div_yield and div_yield > 4:
            return "💰 BUY (Good for Dividends)"
        elif pe_ratio and pe_ratio > 40:
            return "❌ SELL (Overvalued)"
        else:
            return "🤔 HOLD (Needs Further Analysis)"

    except Exception:
        return "🤔 HOLD (Insufficient Data)"

# Function to scrape and display top 5 companies by market cap
def get_top_5_companies():
    """Fetches top companies by market cap from Screener.in"""
    companies = ["TCS", "TATAMOTORS", "INFY", "HCLTECH", "MRF","DRREDDY","TATASTEEL"]
    market_caps = []
    for company in companies:
        data = scrape_screener(company)
        try:
            market_cap = float(data.get('Market Cap', '0').replace(',', ''))
        except ValueError:
            market_cap = 0
        market_caps.append((company, market_cap))
    return market_caps

# Run the scraper when the user clicks "Analyze"
if st.button("Analyze"):
    if stock_name:
        result = scrape_screener(stock_name)

        if "Error" in result:
            st.error(result["Error"])
        else:
            st.subheader(f"📊 Analysis for {result['Company Name']}")
            st.write(f"**Market Cap:** {result['Market Cap']}")
            st.write(f"**Current Price:** {result['Current Price']}")
            st.write(f"**52-Week High/Low:** {result['High / Low']}")
            st.write(f"**Stock P/E:** {result['Stock P/E']}")
            st.write(f"**Dividend Yield:** {result['Dividend Yield']}")
            st.write(f"**ROCE:** {result['ROCE']}")
            st.write(f"**ROE:** {result['ROE']}")
            st.markdown(f"### 📌 Recommendation: **{result['Recommendation']}**", unsafe_allow_html=True)

            # Top 5 Companies Market Cap Chart
            st.subheader("📈 Top 5 Companies by Market Cap")
            top_5 = get_top_5_companies()
            names, caps = zip(*top_5)
            plt.figure(figsize=(8,5))
            plt.bar(names, caps, color=['blue', 'green', 'red', 'purple', 'orange'])
            plt.xlabel("Company")
            plt.ylabel("Market Cap (in Crores)")
            plt.title("Top 5 Companies by Market Cap")
            st.pyplot(plt)
    else:
        st.warning("⚠️ Please enter a valid stock symbol!")
