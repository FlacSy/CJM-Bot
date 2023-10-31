import disnake
from disnake.ext import commands
from main import conn, cursor
import random

cursor.execute('''CREATE TABLE IF NOT EXISTS game_room (
                  server_id INTEGER PRIMARY KEY,
                  channel_id INTEGER,
                  last_channel_number INTEGER DEFAULT 0
               )''')

conn.commit()

class GameRoom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    def get_next_channel_number(self, server_id):
        cursor.execute('SELECT last_channel_number FROM game_room WHERE server_id = ?', (server_id,))
        result = cursor.fetchone()
        if result:
            return result[0] + 1
        return 1

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def set_game_room_channel(self, ctx, channel: disnake.VoiceChannel):
        if ctx.guild:
            server_id = ctx.guild.id
            channel_id = channel.id
            cursor.execute('INSERT OR REPLACE INTO game_room (server_id, channel_id, last_channel_number) VALUES (?, ?, ?)', (server_id, channel_id, 1))
            conn.commit()
            await ctx.send('Успешно добавлен канал игровой комнаты!', ephemeral=True)
        else:
            await ctx.send('Вы должны использовать эту команду на сервере Discord.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
            server_id = member.guild.id
            cursor.execute('SELECT channel_id, last_channel_number FROM game_room WHERE server_id = ?', (server_id,))
            result = cursor.fetchone()
            if result:
                game_room_channel_id = result[0]
                if after.channel.id == game_room_channel_id:
                    category = after.channel.category
                    guild = member.guild
                    channel_number = self.get_next_channel_number(server_id)
                    emoji_list = ['🎮','🕹️','🎰','🎲','🎯','🥊', '🔫']
                    emoji = random.choice(emoji_list)
                    channel_name = f'◦ Игровая {emoji}'
                    new_channel = await guild.create_voice_channel(name=channel_name, category=category, user_limit=99)
                    cursor.execute('UPDATE game_room SET last_channel_number = ? WHERE server_id = ?', (channel_number, server_id))
                    conn.commit()
                    await member.move_to(new_channel)
                    await new_channel.set_permissions(member, manage_channels=True, manage_roles=True)

                    def check(x, y, z):
                        return len(new_channel.members) == 0

                    await self.client.wait_for('voice_state_update', check=check)
                    await new_channel.delete()

def setup(client):
    client.add_cog(GameRoom(client))
