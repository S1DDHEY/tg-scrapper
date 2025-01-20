from telethon import TelegramClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Initialize the Telegram client
client = TelegramClient('anon', API_ID, API_HASH)

# Function to scrape messages and save only new ones to a file
async def scrape_message(client, channel, processed_ids, limit=100):
    # File to save messages
    file_path = "./data/scraped_messages.txt"
    # Open the file in append mode
    with open(file_path, "a", encoding="utf-8") as f:
        async for message in client.iter_messages(channel, limit):
            if message.id not in processed_ids and message.text:
                processed_ids.add(message.id)  # Add message ID to the set
                f.write(message.text + "\n")
                f.write("-" * 100 + "\n")
                print("Fetching...")
                # print(message.text)
                # print("-" * 50)

# Function to run the scraper indefinitely
async def main():
    channel_link = 'https://t.me/solanascanner'
    processed_ids = set()  # To track processed message IDs
    while True:
        try:
            await scrape_message(client, channel_link, processed_ids, limit=10)
            await asyncio.sleep(5)  # Fetch every 5 seconds
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)  # Short delay before retrying in case of error

# Start the client and run the scraper
with client:
    client.loop.run_until_complete(main())
