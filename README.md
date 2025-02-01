# Real-Time-Share-Price-Scraping-and-Analysis 📊

This project is a **Real-Time-Share-Price-Scraping-and-Analysis** built using **Streamlit**, **BeautifulSoup**, and **Pandas**. It allows users to input a stock symbol and retrieve financial data along with a sentiment recommendation (BUY, SELL, or HOLD). The sentiment is based on key financial indicators like **P/E ratio**, **ROCE**, **ROE**, **Dividend Yield**, and more.

## Features

- Scrapes financial data of stocks from [Screener.in](https://www.screener.in/).
- Analyzes the stock's fundamentals such as **Market Cap**, **Stock P/E**, **Dividend Yield**, **ROCE**, **ROE**, and **52-Week High/Low**.
- Provides recommendations: **BUY**, **SELL**, **HOLD**, or **WAIT**, based on the sentiment derived from financial indicators.
- Simple and interactive user interface built with **Streamlit**.

## How It Works

1. **User Input**: The user enters a stock symbol (e.g., TCS, RELIANCE, INFY) in the input field.
2. **Data Scraping**: The application scrapes financial data from the stock's page on **Screener.in**.
3. **Data Extraction**: The key financial values (Market Cap, Stock P/E, etc.) are extracted from the page using **BeautifulSoup**.
4. **Sentiment Analysis**: Based on predefined conditions, the stock is categorized as:
   - ✅ **BUY** (Good Fundamentals)
   - ⏳ **WAIT** (Too Expensive)
   - 📉 **BUY** (Undervalued)
   - 💰 **BUY** (Good for Dividends)
   - ❌ **SELL** (Overvalued)
   - 🤔 **HOLD** (Needs Further Analysis)
5. **Result Display**: The user gets a summary of the stock's financial data and the sentiment recommendation.

## Prerequisites

- Python 3.x
- Libraries:
  - `streamlit` for building the web interface.
  - `requests` for making HTTP requests.
  - `beautifulsoup4` for parsing HTML and extracting data.
  - `pandas` for handling data.

You can install the required libraries using the following command:

```bash
pip install streamlit requests beautifulsoup4 pandas

Example Use
Enter a stock symbol (e.g., TCS) in the input field.
Click the Analyze button.
View the results: stock details like Market Cap, Stock P/E, Dividend Yield, etc., along with the sentiment recommendation (BUY, SELL, HOLD, etc.).



### Explanation:
- **Project Overview**: The description provides a general overview of the purpose and functionality of the project.
- **How It Works**: A simple, step-by-step explanation of the process from input to output.
- **Prerequisites**: Instructions for setting up the environment and installing necessary dependencies.
- **How to Run**: Clear steps to clone the repo, install dependencies, and run the app.
- **Example Use**: An example walk-through of how users can interact with the app.
- **Contributing**: Encourages others to contribute to the project.
- **License**: Specifies the licensing under which the project is made available.

This structure should give your users a clear understanding of how to use the project and how to contribute.
