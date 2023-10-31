import disnake
from disnake.ext import commands
import asyncio
import sqlite3
from main import conn, cursor



cursor.execute('''CREATE TABLE IF NOT EXISTS welcome (
                  server_id INTEGER PRIMARY KEY,
                  channel_id INTEGER,
                  embed_text TEXT,
                  image_url TEXT
               )''')
conn.commit()

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def welcomemessage(self, ctx, channel: disnake.TextChannel, *, embed_text: str, image_url=None):
        cursor.execute("INSERT OR REPLACE INTO welcome (server_id, channel_id, embed_text, image_url) VALUES (?, ?, ?, ?)", (ctx.guild.id, channel.id, embed_text, image_url))
        conn.commit()
        await ctx.send(f'Настройки приветственного сообщения сохранены для сервера {ctx.guild.name}')
        cursor.execute("SELECT embed_text, image_url, channel_id FROM welcome WHERE server_id = ?", (ctx.guild.id,))
        result = cursor.fetchone()
        if result:
            embed_text, saved_image_url, channel_id = result
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                member = ctx.author
                embed = disnake.Embed(title=f'Привет {member.display_name}\nДобро пожаловать на {ctx.guild.name}', description=embed_text)
                if saved_image_url and saved_image_url != "None":
                    embed.set_image(url=saved_image_url)
                await channel.send("Вот как оно будет выглядеть", ephemeral=True)
                await channel.send(embed=embed, ephemeral=True)



    @commands.Cog.listener()
    async def on_member_join(self, member):
        # print(f"Пользователь {member.display_name} присоединился к серверу {member.guild.name}")
        cursor.execute("SELECT embed_text, image_url, channel_id FROM welcome WHERE server_id = ?", (member.guild.id,))
        result = cursor.fetchone()
        if result != "None":
            embed_text, image_url, channel_id = result
            # print(f"Найдены данные для приветственного сообщения: embed_text={embed_text}, image_url={image_url}, channel_id={channel_id}")
            channel = member.guild.get_channel(channel_id)
            if channel:
                embed = disnake.Embed(title=f'Привет {member.display_name}\nДобро пожаловать на {member.guild.name}', description=embed_text)
                if image_url:
                    embed.set_image(url=image_url)
                await channel.send(embed=embed)
        else:
            None


def setup(client):
    client.add_cog(Welcome(client))