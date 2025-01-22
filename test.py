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
OUTPUT_FILE = "./data/extracted_addresses.csv"

# Function to scrape messages and save all unique ones
async def scrape_messages(client, channel, processed_ids, limit=100):
    new_messages = []
    
    async for message in client.iter_messages(channel, limit):
        if message.id not in processed_ids and message.text:
            processed_ids.add(message.id)  # Track processed messages
            new_messages.append(message.text.strip())

    # Save all new unique messages
    if new_messages:
        with open(SCRAPED_FILE, "a", encoding="utf-8") as f:
            for msg in new_messages:
                f.write(msg + "\n" + "-" * 100 + "\n")
        print(f"📄 Successfully saved {len(new_messages)} messages to {SCRAPED_FILE}")

        # Extract and save addresses after each new batch
        extract_and_save_addresses()

# Function to extract addresses and save to CSV
def extract_and_save_addresses():
    # Read the file
    with open(SCRAPED_FILE, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Regex pattern to match bolded "Address:" followed by backtick-enclosed text
    pattern = r"\*\*Address:\s*\*\*\s*`([^`]+)`"
    
    # Find all matches
    matches = re.findall(pattern, content)
    
    # Save matches to a CSV file
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Address"])  # Write the header
        for address in matches:
            writer.writerow([address])
    
    print(f"✅ Extracted addresses have been saved to {OUTPUT_FILE}")

# Function to run scraping in a loop
async def main():
    channel_link = 'https://t.me/solanascanner'
    processed_ids = set()

    while True:
        try:
            await scrape_messages(client, channel_link, processed_ids, limit=10)
            await asyncio.sleep(5)  # Fetch every 5 seconds
        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(10)  # Short delay before retrying

# Start the client and run the script
with client:
    client.loop.run_until_complete(main())
