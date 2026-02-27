import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# The make_graph function has been modified to use Matplotlib for static graphs. Earlier, it used Plotly to generate interactive dashboards, which caused issues when uploading the notebook in the MARK assignment submission.

import matplotlib.pyplot as plt

def make_graph(stock_data, revenue_data, stock):
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Stock price
    axes[0].plot(pd.to_datetime(stock_data_specific.Date), stock_data_specific.Close.astype("float"), label="Share Price", color="blue")
    axes[0].set_ylabel("Price ($US)")
    axes[0].set_title(f"{stock} - Historical Share Price")

    # Revenue
    axes[1].plot(pd.to_datetime(revenue_data_specific.Date), revenue_data_specific.Revenue.astype("float"), label="Revenue", color="green")
    axes[1].set_ylabel("Revenue ($US Millions)")
    axes[1].set_xlabel("Date")
    axes[1].set_title(f"{stock} - Historical Revenue")

    plt.tight_layout()
    plt.show()


tesla_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
gme_url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

def get_stock_and_revenue(ticker_symbol, revenue_url):
    # Stock
    ticker = yf.Ticker(ticker_symbol)
    stock_data = ticker.history(period="max")
    
    # Revenue
    html = requests.get(revenue_url).text
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    revenue_table = tables[1]
    revenue_data = pd.DataFrame(columns=["Date", "Revenue"])
    
    for row in revenue_table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        date = cols[0].text
        revenue = cols[1].text
        revenue_data = pd.concat(
            [revenue_data, pd.DataFrame({"Date":[date], "Revenue":[revenue]})],
            ignore_index=True
        )
        
    revenue_data["Revenue"] = revenue_data['Revenue'].str.replace(r',|\$', "", regex=True)
    revenue_data.dropna(inplace=True)
    revenue_data = revenue_data[revenue_data['Revenue'] != ""]
    
    return stock_data, revenue_data


tesla_data, tesla_revenue = get_stock_and_revenue("TSLA", tesla_url)
gme_data, gme_revenue = get_stock_and_revenue("GME", gme_url)


# Ask user if they want to save the HTML files
while True:
  save_html = input("Do you want to save HTML files for Tesla and GameStop? (Y/N): ").strip().upper()
  if save_html in ["Y", "N"]:
    break
  else:
    print("Please enter 'Y' for Yes or 'N' for No.")

if save_html == "Y":
    # Create folder if it doesn't exist
    os.makedirs("HTML_files", exist_ok=True)

    # Save Tesla tables
    tesla_data.to_html("HTML_files/Tesla_data.html", index=False)
    tesla_revenue.to_html("HTML_files/Tesla_revenue.html", index=False)

    # Save GameStop tables
    gme_data.to_html("HTML_files/GME_data.html", index=False)
    gme_revenue.to_html("HTML_files/GME_revenue.html", index=False)

    print("All HTML files created in the 'HTML_files' folder!")

else:
    print("HTML files not saved.")