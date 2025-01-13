from telethon import TelegramClient
import os
import asyncio

# Replace these with your actual API ID and hash
API_ID = "25590517"
API_HASH = "6b57414d43f506d957bff007f1cb618c"

# Initialize the Telegram client
client = TelegramClient('anon', API_ID, API_HASH)

# Function to scrape messages and save to a file
async def scrape_message(client, channel, limit=100):
    # File to save messages
    file_path = "scraped_messages.txt"
    # Open the file in append mode
    with open(file_path, "a", encoding="utf-8") as f:
        # Iterate over messages
        async for message in client.iter_messages(channel, limit):
            if message.text:
                f.write(message.text + "\n")
                f.write("-" * 50 + "\n")
                print(message.text)  # Print to console
                print("-" * 50)

# Function to run the scraper indefinitely
async def main():
    channel_link = 'https://t.me/solanascanner'
    while True:
        try:
            await scrape_message(client, channel_link, limit=10)
            # Delay between iterations to avoid spamming
            await asyncio.sleep(30)  # Adjust the sleep time as needed
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)  # Short delay before retrying

# Start the client and run the scraper
with client:
    client.loop.run_until_complete(main())
