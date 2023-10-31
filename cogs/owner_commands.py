import disnake 
from disnake.ext import commands  
from config.config import *

'''Функция для выведения ошибок когов'''
async def cog_error(ctx, error):
    await ctx.send(f"Ошибка: {error}", ephemeral=True)


class OwnerCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    @commands.command()
    async def maintenance(self, ctx, status):
        if ctx.author.id == owner_id:
            try:
                if status == 'on':
                    status_activity = disnake.Game("👷‍♂️ТЕХНИЧИЧЕСКИЕ РАБОТЫ🚧")
                    await self.client.change_presence(status=disnake.Status.idle, activity=status_activity)
                    await ctx.send(f'<:icons8toolbox64:1157819680636014664>Режим техничиских работ включён<:icons8toolbox64:1157819680636014664>')
                elif status == 'off':
                    await self.client.change_presence(status=disnake.Status.online)
                    await ctx.send(f'<:icons8toolbox64:1157819680636014664>Режим техничиских работ выключён<:icons8toolbox64:1157819680636014664>')

                elif status == False or status == None:
                    await ctx.send('Используйте "maintenance on/off"', ephemeral=True)
                    
            except Exception as eror:
                print(f'Произошла ошибка:\n{eror}')

    @commands.command()
    async def status(self, ctx, status):
        if ctx.author.id == owner_id:
            status_activity = disnake.Game(status)
            await self.client.change_presence(activity=status_activity) 

    @commands.command()
    async def clear_status(self, ctx):
        if ctx.author.id == owner_id:           
            await self.client.change_presence(status=disnake.Status.online) 

    '''Команда для загрузки когов'''
    @commands.slash_command(name = 'load', guild_ids=[dev_guild])
    async def load(self, ctx, extension):
        if ctx.author.id == owner_id:
            try:
                await ctx.send("Загрузка...", ephemeral=True)
                self.client.load_extension(f"cogs.{extension}")
                print(f'Ког {extension} загружен...')
            except Exception as error:
                await cog_error(ctx, error)
                
    '''Команда для выгрузки когов'''
    @commands.slash_command(name = 'unload', guild_ids=[dev_guild])
    async def unload(self, ctx, extension):
        if ctx.author.id == owner_id:
            try:
                await ctx.send("Выгрузка...", ephemeral=True)
                self.client.unload_extension(f"cogs.{extension}")
                print(f'Ког {extension} выгружен...')
            except Exception as error:
                await cog_error(ctx, error)

    '''Команда для перезагрузки когов'''
    @commands.slash_command(name = 'reload', guild_ids=[dev_guild])
    async def reload(self, ctx, extension):
        if ctx.author.id == owner_id:
            try:
                await ctx.send("Перезагрузка...", ephemeral=True)
                self.client.unload_extension(f"cogs.{extension}")
                self.client.load_extension(f"cogs.{extension}")
                print(f'Ког {extension} перезагружен...')   
            except Exception as error:
                await cog_error(ctx, error)

def setup(client):
    client.add_cog(OwnerCommands(client))