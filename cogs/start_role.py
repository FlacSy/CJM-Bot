import disnake
from disnake.ext import commands
import asyncio
import sqlite3
from main import conn, cursor



cursor.execute('''CREATE TABLE IF NOT EXISTS start_role (
                  server_id INTEGER PRIMARY KEY,
                  role_id INTEGER
               )''')
conn.commit()

class StarRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def start_role(self, ctx, role_id):
        cursor.execute("INSERT OR REPLACE INTO start_role (server_id, role_id) VALUES (?, ?)", (ctx.guild.id, int(role_id)))
        conn.commit()
        await ctx.send(f'Настройки роли по умолчанию установлены для {ctx.guild.name}.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor.execute("SELECT role_id FROM start_role WHERE server_id = ?", (member.guild.id,))
        result = cursor.fetchone()
        if result:
            role_id = result[0]  
            role = disnake.utils.get(member.guild.roles, id=role_id)
            if role:
                await member.add_roles(role)
            else:
                print(f"Роль с ID {role_id} не найдена на сервере.")
        else:
            print("Данные для начальной роли не найдены на сервере.")

def setup(bot):
    bot.add_cog(StarRole(bot))