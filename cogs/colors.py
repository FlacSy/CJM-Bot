import disnake 
from disnake.ext import commands  
from config.config import *
from main import conn, cursor



cursor.execute('''CREATE TABLE IF NOT EXISTS colors (
                  server_id INTEGER PRIMARY KEY,
                  channel_id INTEGER
               )''')

conn.commit()

heart_colors =[
    "❤️",  
    "🧡",  
    "💛",  
    "💚",  
    "💙",  
    "💜",
    "🖤"
]
    
class Colors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def setcolorschannel(self, ctx, channel: disnake.TextChannel):
        if ctx.guild:
            server_id = ctx.guild.id
            channel_id = channel.id
            cursor.execute('INSERT OR REPLACE INTO colors (server_id, channel_id) VALUES (?, ?)', (server_id, channel_id))
            conn.commit()

            await ctx.send('Успешно добавлен канал для выбора цветов!', ephemeral=True)

            server = self.client.get_guild(server_id)
            channel = self.client.get_channel(channel_id)

 
            existing_roles = {role.name: role for role in server.roles}
            for color in heart_colors:
                if color not in existing_roles:
                    try:
                        role = await server.create_role(name=color)
                        color_hex = {
                            "❤️": 0xFF0000,
                            "🧡": 0xFFA500,
                            "💛": 0xFFFF00,
                            "💚": 0x00FF00,
                            "💙": 0x0000FF,
                            "💜": 0x800080,
                            "🖤": 0x000000
                        }.get(color)
                        if color_hex is not None:
                            await role.edit(color=color_hex)

                    except Exception as error:
                        await channel.send(f'Произошла ошибка при создании ролей: "{error}"\n. Отправьте это в команду /bug либо напишите для <@997492642587873360>')

            try:
                embed = disnake.Embed(title='Выбери цвет', color=0xBF00FF)
                embed.set_image(url='https://cdn.disnakeapp.com/attachments/1158126815991308521/1160276146756272218/img-8dljPclAKmLp4aeGD3TFGuKS.png?ex=6534125e&is=65219d5e&hm=cb393ffdca0652825b8e866b96a844c2c5a21164d4f4f456b52b3616a04fe3f8&')
                message = await channel.send(embed=embed)
                for color in heart_colors:
                    await message.add_reaction(color)
            except Exception as error:
                await channel.send(f'Произошла ошибка при отправки авто ролей: "{error}"\n. Отправьте это в команду /bug либо напишите для <@997492642587873360>')
        else:
            await ctx.send('Вы должны использовать эту команду на сервере disnake.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        if guild_id:
            server_id = guild_id
            cursor.execute('SELECT channel_id FROM colors WHERE server_id = ?', (server_id,))
            result = cursor.fetchone()

            if result and payload.channel_id == result[0]:  
                guild = self.client.get_guild(guild_id)
                message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)

                if message.author.id == self.client.user.id:  
                    if payload.user_id != self.client.user.id and payload.emoji.name in heart_colors:
                        member = guild.get_member(payload.user_id)
                        if member:
                            role_name = heart_colors[heart_colors.index(payload.emoji.name)]
                            role = disnake.utils.get(guild.roles, name=role_name)

                            if role:
                                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild_id = payload.guild_id
        if guild_id:
            server_id = guild_id
            cursor.execute('SELECT channel_id FROM colors WHERE server_id = ?', (server_id,))
            result = cursor.fetchone()

            if result and payload.channel_id == result[0]:  
                guild = self.client.get_guild(guild_id)
                message = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)

                if message.author.id == self.client.user.id: 
                    if payload.user_id != self.client.user.id and payload.emoji.name in heart_colors:
                        member = guild.get_member(payload.user_id)
                        if member:
                            role_name = heart_colors[heart_colors.index(payload.emoji.name)]
                            role = disnake.utils.get(guild.roles, name=role_name)

                            if role:
                                await member.remove_roles(role)


def setup(client):
    client.add_cog(Colors(client))