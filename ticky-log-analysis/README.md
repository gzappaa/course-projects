Ticky Log Analysis

Process system logs (syslog.log) to generate error and user activity reports. Convert CSV reports to HTML for easy viewing in your browser.

Requirements

Docker Desktop for Windows

(Optional) Python 3.11+ if you want to run scripts locally

Project Structure
ticky-log-analysis/
├─ data/         # Logs and CSVs
│  └─ syslog.log
├─ html/         # Generated HTML reports
├─ scripts/      # Helper scripts
│  └─ csv_to_html.py
├─ src/          # Main script
│  └─ ticky_check.py
├─ Dockerfile
└─ README.md

Run with Docker (Windows PowerShell)

Build the Docker image:

docker build -t ticky-log-analysis .


Run the container (mount local folders for CSVs and HTMLs):

docker run --rm `
  -v ${PWD}\data:/app/data `
  -v ${PWD}\html:/app/html `
  ticky-log-analysis


✅ This will generate:

data/error_message.csv

data/user_statistics.csv

html/errors.html

html/users.html

Open the HTML reports in your browser:

start html\errors.html
start html\users.html

Run Locally (without Docker)

If you have Python installed, you can also run everything locally:

Generate CSVs:

python .\src\ticky_check.py


Convert CSVs to HTML:

python .\scripts\csv_to_html.py .\data\error_message.csv .\html\errors.html
python .\scripts\csv_to_html.py .\data\user_statistics.csv .\html\users.html


Open HTML in browser:

start .\html\errors.html
start .\html\users.html