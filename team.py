from telethon import TelegramClient, events
import logging
import asyncio
import re

# Replace these with your credentials
api_id = '27232480'
api_hash = 'b00b2f81b37e64a7eca45f11570ed7ac'
bot_token = '7245992910:AAFjz_Klm6CWR2X2uORIydulKZ8a8WBqswg'
phone_number = '+17169079367'
session_file = 'session_name'
source_group_ids = [ -4198424207 , -1002243936664, -1001371184682, 6145463489, -1002208686405, -1002237728660]
destination_group_id = -1002208686405

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define your filter
def message_passes_filter(message_text):
    # Check for presence of specific keywords or phrases
    keywords = ['Oct', 'Nov', 'Dec', 'Available', 'September', 'October', 'Sep', 'November']
    pattern = re.compile('|'.join(keywords), re.IGNORECASE)
    return bool(pattern.search(message_text))

async def main():
    client = TelegramClient(session_file, api_id, api_hash)
    auth_code = 85997
    
    try:
        # Connect and sign in
        await client.start(phone_number)

    except EOFError:
        if auth_code:
            logging.info("Authentication code required. Using predefined code.")
            try:
                await client.sign_in(phone_number, auth_code)
            except Exception as e:
                logging.error(f"An error occurred during sign-in with predefined code: {e}")
                return  # Exit if sign-in fails
        else:
            logging.error("Authentication code required but not provided.")
            return  # Exit if no code is provided

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return  # Exit if an unexpected error occurs

    @client.on(events.NewMessage(chats= source_group_ids))
    async def handler(event):
        message = event.message
        chat = await client.get_entity(message.chat_id)
        message_id = message.id
        message_text = message.text or ""

        if message.media:
            # Construct the link to the media message
            user_name = chat.username
            message_id = message.id
            message_url = f"https://t.me/{chat.username}/{message_id}"

            # Send the link to the private chat
            try:
                await client.send_message(destination_group_id, f"Screen Shot link: \n {message_url}")
                logging.info(f"Message URL: {message_url}")
            except Exception as e:
                logging.error(f"An error occurred while sending the media link: {e}")
        elif message_passes_filter(message_text):
            # If it's a text message and passes the filter
            try:
                await client.send_message(destination_group_id, message_text)
                logging.info(f"Message sent: {message_text}")
            except Exception as e:
                logging.error(f"An error occurred while sending the message: {e}")
        else:
            logging.info(f"Message did not pass filter: {message_text}")

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
