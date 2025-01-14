import re
import csv

# File paths
input_file_path = "./data/scraped_messages.txt"
output_file_path = "./data/extracted_addresses.csv"

# Read the file
with open(input_file_path, "r", encoding="utf-8") as file:
    content = file.read()

# Regex pattern to match bolded "Address:" followed by backtick-enclosed text
pattern = r"\*\*Address:\s*\*\*\s*`([^`]+)`"

# Find all matches
matches = re.findall(pattern, content)

# Save matches to a CSV file
with open(output_file_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Address"])  # Write the header
    for address in matches:
        writer.writerow([address])

print(f"Extracted addresses have been saved to {output_file_path}")
