import disnake
from disnake.ext import commands
import sqlite3
import asyncio
from datetime import datetime
from main import conn, cursor

cursor.execute('''CREATE TABLE IF NOT EXISTS message_data (
                  user_id INTEGER PRIMARY KEY,
                  message_count INTEGER,
                  guild_id INTEGER 
               )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS user_levels (
                  user_id INTEGER PRIMARY KEY,
                  message_count INTEGER,
                  level INTEGER
               )''')

class Liders(commands.Cog):
    def __init__(self, client, conn):
        self.client = client
        self.conn = conn
        self.leaderboard_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    @commands.slash_command()
    async def top(self, ctx, num=None):
        if num is None:
            num = 10
        else:
            num = int(num)

        cursor = self.conn.cursor() 
        cursor.execute('SELECT * FROM message_data ORDER BY message_count DESC LIMIT ?', (num,))
        top_messages = cursor.fetchall()

        formatted_messages = [f'{idx+1}. <@{message[0]}> - {message[1]} сообщений' for idx, message in enumerate(top_messages)]
        embed = disnake.Embed(title='Топ: ', description='\n'.join(formatted_messages))
        await ctx.send(embed=embed, ephemeral=True)

    @commands.slash_command()
    async def my_top(self, ctx):
        user_id = str(ctx.author.id)
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM message_data WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            total_message_count = user_data[1]  
            user_rank = cursor.execute('SELECT COUNT(*) + 1 FROM message_data WHERE message_count > ?', (total_message_count,)).fetchone()[0]
            user_level = total_message_count // 100

            embed = disnake.Embed(
                title="Ваше место в рейтинге",
                description=f"Ваше место в рейтинге: {user_rank}\nКоличество слов: {user_data[1]}\nВаш уровень: {user_level}",
                color=0x3498db
            )
            await ctx.send(embed=embed, ephemeral=True)
        else:
            await ctx.send('You have not sent any messages yet.', ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.author.bot:
            return

        if message.guild is None:
            return

        author_id = str(message.author.id)

        cursor = self.conn.cursor()

        cursor.execute('INSERT OR REPLACE INTO message_data (user_id, message_count, guild_id) VALUES (?, COALESCE((SELECT SUM(message_count) FROM message_data WHERE user_id = ?), 0) + 1, ?)', (author_id, author_id, author_id))

        cursor.execute('SELECT message_count FROM message_data WHERE user_id = ?', (author_id,))
        total_message_count = cursor.fetchone()[0]

        user_level = total_message_count // 100

        cursor.execute('SELECT level FROM user_levels WHERE user_id = ?', (author_id,))
        old_level = cursor.fetchone()

        if old_level is None or old_level[0] != user_level:
            if user_level >= 1:
                embed = disnake.Embed(
                    title=f'Поздравляем, вы достигли {user_level} уровня!',
                    description=f'Вы достигли нового уровня на сервере!',
                    color=0x00ff00
                )
                await message.channel.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title=f'Поздравляем, это ваше первое сообщение!',
                    description=f'Подсказка: 100 сообщений + 1 уровень!',
                    color=0x00ff00
                )
                await message.channel.send(embed=embed)                
        cursor.execute('INSERT OR REPLACE INTO user_levels (user_id, message_count, level) VALUES (?, ?, ?)', (author_id, total_message_count, user_level))

        self.conn.commit()

        await self.client.process_commands(message)
        await asyncio.sleep(3600)
        await self.update_top_messages()
        await self.daily_check()


def setup(client):
    client.add_cog(Liders(client, conn))