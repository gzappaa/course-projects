import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
import lxml

url = "https://en.wikipedia.org/wiki/World_population"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# Get page
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, "html.parser")

# Find the heading
heading = soup.find("h3", {"id": "Most_densely_populated_countries"})

# Get the next table
table = heading.find_next("table")

# Convert to DataFrame
df = pd.read_html(StringIO(str(table)))[0]

# Save as HTML to view online
df.to_html("most_densely_populated.html", index=False)

print(df.head())