# Import necessary libraries
from dotenv import load_dotenv
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys

# Get the API key and token for OPENAI and Telegram
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the model to be used
model_name = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token = TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Temporary Memory of the OPENAI API Model
class Reference:
    '''
    A class to store initial memory from the bot API
    '''
    def __init__(self) -> None:
        self.reference = ""

# Initialize reference
reference = Reference()

def clear_memory():
    '''
    A function that clears the bot's memory from the start of the command
    '''
    reference.response = ""

# Function for start command
@dp.message_handler(commands = ['start'])
async def welcome(message: types.Message):
    '''
This handler receives message using \start command
    '''
    await message.reply("Hi! I am a Robot! How can I assist you?")

# Function for help command
@dp.message_handler(commands = ['help'])
async def helper(message: types.Message):
    '''
This handler receives message using \help command
    '''
    help_command = '''
    Hi there! I am a Telegram Bot powered by OpenAI's GPT-3.5-Turbo Model. I was created by Rob Christian.

Please follow the commands:
/start - to start the conversation
/help - to get this help menu
/clear - to clear any past conversations made from start

Thank you and I hope this helps you.
    '''
    await message.reply(help_command)

# Function for clear command
@dp.message_handler(commands = ['clear'])
async def clear(message: types.Message):
    '''
    This handler clears the memory of the bot made from the start
    '''
    clear_memory()
    await message.reply("Past conversations and context were cleared!!")

@dp.message_handler()
async def bot_app(message: types.Message):
    '''
    This handler uses gpt-3.5-turbo to generate output based on user's input response.
    '''
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = model_name,
        messages = [
            {'role': 'assistant', 'content': reference.response},
            {'role': 'user', 'content': message.text}
        ]
    )
    reference.response = response.choices[0].message.content
    print(f">>> bot_app: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = False)
