from telethon import TelegramClient
import asyncio
import os
import re
import csv
from dotenv import load_dotenv

# Load API credentials from .env file
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Initialize the Telegram client
client = TelegramClient('anon', API_ID, API_HASH)

# File paths
SCRAPED_FILE = "./data/scraped_messages.txt"
EXTRACTED_FILE = "./data/extracted_addresses.csv"

# Regex pattern to extract addresses
ADDRESS_PATTERN = r"\*\*Address:\s*\*\*\s*`([^`]+)`"

# Regex to check for Telegram, X, or any website
SOCIALS_PATTERN = r"(t\.me|Telegram|x\.com|twitter\.com|https?://[^\s]+)"

# Function to scrape messages and save only new ones that match conditions
async def scrape_messages(client, channel, processed_ids, limit=100):
    new_messages = []
    valid_messages = []
    
    async for message in client.iter_messages(channel, limit):
        if message.id not in processed_ids and message.text:
            processed_ids.add(message.id)  # Track processed messages
            
            print(f"Fetched message ID {message.id}: {message.text[:50]}...")  # Debug log
            
            # Check if message contains Telegram, X, or a website
            if re.search(SOCIALS_PATTERN, message.text, re.IGNORECASE):
                valid_messages.append(message.text)  # Store valid messages
                print("✅ Message contains valid socials, saving it!")
            else:
                print("❌ Skipped message (No valid socials found)")

    # Write valid messages to file
    if valid_messages:
        with open(SCRAPED_FILE, "a", encoding="utf-8") as f:
            for msg in valid_messages:
                f.write(msg.strip() + "\n" + "-" * 100 + "\n")
        print(f"📄 Successfully saved {len(valid_messages)} messages to {SCRAPED_FILE}")
    else:
        print("⚠️ No valid messages found, nothing written to file!")

    return valid_messages

# Function to extract addresses and save them to a CSV file
def extract_addresses():
    if not os.path.exists(SCRAPED_FILE):
        print("⚠️ Scraped file does not exist yet.")
        return

    with open(SCRAPED_FILE, "r", encoding="utf-8") as file:
        content = file.readlines()

    extracted_addresses = []
    
    for line in content:
        match = re.search(ADDRESS_PATTERN, line)
        if match:
            extracted_addresses.append(match.group(1))

    if extracted_addresses:
        with open(EXTRACTED_FILE, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Address"])  # Write header
            for address in extracted_addresses:
                writer.writerow([address])
        print(f"📊 Extracted {len(extracted_addresses)} addresses to {EXTRACTED_FILE}")
    else:
        print("⚠️ No addresses found in messages!")

# Function to run both scraping and extraction in a loop
async def main():
    channel_link = 'https://t.me/solanascanner'
    processed_ids = set()

    while True:
        try:
            new_messages = await scrape_messages(client, channel_link, processed_ids, limit=10)
            if new_messages:  # Only extract if new messages were fetched
                extract_addresses()
            await asyncio.sleep(5)  # Fetch every 5 seconds
        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(10)  # Short delay before retrying

# Start the client and run the script
with client:
    client.loop.run_until_complete(main())
