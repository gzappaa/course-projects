import pandas as pd
from bs4 import BeautifulSoup
import requests

# URL containing world population data
url = "https://en.wikipedia.org/wiki/World_population"

# Headers for Requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}

# Get webpage content
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, "html.parser")

# Empty DataFrame
population_data = pd.DataFrame(columns=["Rank", "Country", "Population", "Area", "Density"])

# Find all tables in the page
tables = soup.find_all('table')

# Find the table with the correct title
table_index = None
for index, table in enumerate(tables):
    if "10 most densely populated countries" in str(table):
        table_index = index
        break  # stop after finding the table

if table_index is None:
    print("Table not found!")
else:
    # Iterate over table rows
    for row in tables[table_index].tbody.find_all("tr"):
        col = row.find_all("td")
        if col and len(col) >= 5:  # make sure row has all columns
            rank = col[0].text.strip()
            country = col[1].text.strip()
            population = col[2].text.strip()
            area = col[3].text.strip()
            density = col[4].text.strip()

            # Create a new row as a DataFrame
            new_row = pd.DataFrame([{
                "Rank": rank,
                "Country": country,
                "Population": population,
                "Area": area,
                "Density": density
            }])

            # Add to the main DataFrame
            population_data = pd.concat([population_data, new_row], ignore_index=True)

    # Show the result
    print(population_data)
    # Save HTML file
    population_data.to_html("most_densely_populated.html", index=False)
    print("File 'most_densely_populated.html' created! You can open it in your browser.")