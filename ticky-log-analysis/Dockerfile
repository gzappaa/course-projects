# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy source and scripts into container
COPY src/ src/
COPY scripts/ scripts/

# Make sure data and html folders exist
RUN mkdir -p /app/data /app/html

# Default command: generate CSVs and HTMLs
CMD python3 src/ticky_check.py && \
    python3 scripts/csv_to_html.py /app/data/error_message.csv /app/html/errors.html && \
    python3 scripts/csv_to_html.py /app/data/user_statistics.csv /app/html/users.html
