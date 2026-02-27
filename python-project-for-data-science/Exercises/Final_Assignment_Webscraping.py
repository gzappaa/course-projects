import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
import sys  # to exit the program with an error

# Ignore pandas FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

# URLs for Netflix and Amazon data
urls = {
    "netflix": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html",
    "amazon":  "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/amazon_data_webpage.html"
}

# Ask the user which company they want
company = input("Enter 'netflix' or 'amazon': ").strip().lower()

# Exit the program if the input is not valid
if company not in urls:
    sys.exit("Error: you must enter either 'netflix' or 'amazon'.")

# Get the correct URL
url = urls[company]

# Download the HTML page
html_data = requests.get(url).text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_data, 'html.parser')

# Create an empty DataFrame with the correct columns
data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])

# Loop through each row in the table body
for row in soup.find("tbody").find_all('tr'):
    cols = row.find_all("td")
    date = cols[0].text
    Open = cols[1].text
    high = cols[2].text
    low = cols[3].text
    close = cols[4].text
    adj_close = cols[5].text
    volume = cols[6].text

    # Append the row to the DataFrame
    data = pd.concat([data, pd.DataFrame({
        "Date":[date],
        "Open":[Open],
        "High":[high],
        "Low":[low],
        "Close":[close],
        "Adj Close":[adj_close],
        "Volume":[volume]
    })], ignore_index=True)

# Display the first 5 rows of the DataFrame
print(data.head())
# Save HTML file
data.to_html(f"{company}_data.html", index=False)
print(f"File '{company}_data.html' created! You can open it in your browser.")