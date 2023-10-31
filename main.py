import disnake
from disnake.ext import commands
import os
from config.config import *
import asyncio
import sqlite3
from art import tprint 
from colorama import init
init()
from colorama import Fore, Back, Style

conn = sqlite3.connect('bot_data.db')
cursor = conn.cursor()


'''Объявление клиента'''
intents = disnake.Intents.all()
intents.voice_states = True
client = commands.Bot(command_prefix="cl.", intents=intents)

@client.event
async def on_ready():
    tprint(client.user.name)
    print('------')


'''Функция для запуска бота'''
def main():
    
    for filename in os.listdir("./cogs"):

        if filename.endswith('.py'):
            client.load_extension(f"cogs.{filename[:-3]}")
    client.run(TOKEN)

'''Проверка, запущен ли файл, а не импортирован'''
if __name__ == '__main__':   
    main()