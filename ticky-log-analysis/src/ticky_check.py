#!/usr/bin/env python3

import csv
import re
import os
import operator


IN_DOCKER = os.path.exists("/app")
# Paths
if IN_DOCKER:
    LOG_FILE = "/app/data/syslog.log"
    ERROR_CSV = "/app/data/error_message.csv"
    USER_CSV = "/app/data/user_statistics.csv"
else:
    LOG_FILE = "data/syslog.log"
    ERROR_CSV = "data/error_message.csv"
    USER_CSV = "data/user_statistics.csv"

# Dictionaries to store info
error_counts = {}
user_stats = {}

# Regex patterns
error_pattern = re.compile(r"ticky: ERROR ([\w ']+)")
info_pattern = re.compile(r"ticky: INFO [\w ]* \[#\d+\] \(([\w\.]+)\)")
user_pattern = re.compile(r"\(([\w\.]+)\)$")

# Read log file
with open(LOG_FILE, "r") as file:
    for line in file:
        # Match ERROR
        error_match = error_pattern.search(line)
        if error_match:
            error_msg = error_match.group(1)
            user_match = user_pattern.search(line)
            username = user_match.group(1) if user_match else "unknown"

            # Count error occurrences
            if error_msg in error_counts:
                error_counts[error_msg] += 1
            else:
                error_counts[error_msg] = 1

            # Count per user
            if username not in user_stats:
                user_stats[username] = {"INFO": 0, "ERROR": 1}
            else:
                user_stats[username]["ERROR"] += 1

        # Match INFO
        info_match = info_pattern.search(line)
        if info_match:
            username = info_match.group(1)
            if username not in user_stats:
                user_stats[username] = {"INFO": 1, "ERROR": 0}
            else:
                user_stats[username]["INFO"] += 1

# Sort errors by count descending
sorted_errors = sorted(error_counts.items(), key=operator.itemgetter(1), reverse=True)

# Sort users by username
sorted_users = sorted(user_stats.items(), key=operator.itemgetter(0))

# Ensure data directory exists
os.makedirs(os.path.dirname(ERROR_CSV), exist_ok=True)

# Write error CSV
with open(ERROR_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Error", "Count"])
    for error, count in sorted_errors:
        writer.writerow([error, count])

# Write user CSV
with open(USER_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Username", "INFO", "ERROR"])
    for user, counts in sorted_users:
        writer.writerow([user, counts["INFO"], counts["ERROR"]])

print("Reports generated:")
print(f"- {ERROR_CSV}")
print(f"- {USER_CSV}")
