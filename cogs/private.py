import disnake
from disnake.ext import commands
import asyncio
import sqlite3
from main import conn, cursor
import random 


cursor.execute('''CREATE TABLE IF NOT EXISTS private (
                  server_id INTEGER PRIMARY KEY,
                  channel_id INTEGER
               )''')

conn.commit()


class Private(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def setprivatechannel(self, ctx, channel: disnake.VoiceChannel):
        if ctx.guild:
            server_id = ctx.guild.id
            channel_id = channel.id
            cursor.execute('INSERT OR REPLACE INTO private (server_id, channel_id) VALUES (?, ?)', (server_id, channel_id))
            conn.commit()  
            await ctx.send('Успешно добавлен приватный канал!', ephemeral=True)
        else:
            await ctx.send('Вы должны использовать эту команду на сервере Discord.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            server_id = member.guild.id
            cursor.execute('SELECT channel_id FROM private WHERE server_id = ?', (server_id,))
            result = cursor.fetchone()
            if result:
                private_channel_id = result[0]

                if after.channel.id == private_channel_id:
                    category = after.channel.category
                    guild = member.guild
                    emoji_list = ['✨','💡','💛','💫','🥰','🤩','🫦']
                    emoji = random.choice(emoji_list)
                    channel = await guild.create_voice_channel(name=f'◦ Приват {member.display_name} {emoji}', category=category, user_limit=2)  
                    await member.move_to(channel)
                    await channel.set_permissions(member, manage_channels=True, manage_roles=True)

                    def check(x, y, z):
                        return len(channel.members) == 0

                    await self.client.wait_for('voice_state_update', check=check)
                    await channel.delete()

def setup(bot):
    bot.add_cog(Private(bot))