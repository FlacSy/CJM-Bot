import disnake
from disnake.ext import commands
from config.config import *
import requests
from bs4 import BeautifulSoup
import random
from translate import Translator
from rule34Py import rule34Py

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client


    '''Обявление эвента'''
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')


    '''Обявление команнды'''
    @commands.slash_command(name='bug', description='Сообщить о баге')
    async def bug(self, ctx, bug_text: str, link: str = None):
        owner = self.client.get_user(owner_id)

        if owner is not None:
            user = ctx.user 
            embed = disnake.Embed(title=f'**БАГ**', color=0xfc237e)
            embed.add_field(name=f"**Сообщил {user.display_name}**", value=bug_text, inline=False)
            if link:
                embed.add_field(name="**Ссылка**", value=link, inline=False)
            else:
                embed.add_field(name="**Ссылка**", value='Отсутствует', inline=False)
            await owner.send(embed=embed)
            embed = disnake.Embed(title='Баг успешно отправлен!', color=0xa43bff)
            await ctx.send(embed=embed, ephemeral=True)
        else:
            await ctx.send('Не удалось найти канал для отправки бага.', ephemeral=True)


    @commands.slash_command(name='idea', description='Предложить идею')
    async def idea(self, ctx, idea_text: str, link: str = None):

        owner = self.client.get_user(owner_id)
        if owner is not None:
            user = ctx.user 
            embed = disnake.Embed(title=f'**Новая идея!**', color=0x3bf2ff)
            embed.add_field(name=f"**от {user.display_name}**", value=idea_text, inline=False)
            if link:
                embed.add_field(name="**Ссылка**", value=link, inline=False)
            else:
                embed.add_field(name="**Ссылка**", value='Отсутствует', inline=False)
            await owner.send(embed=embed)
            embed = disnake.Embed(title='Идея успешно отправлена!', color=0xa43bff)
            await ctx.send(embed=embed, ephemeral=True)
        else:
            await ctx.send('Не удалось найти канал для отправки идеи.', ephemeral=True)

    @commands.slash_command(name='r34', description='Поиск на rule34')
    async def r34(self, ctx, tags: str):
        if not ctx.channel.is_nsfw():
            await ctx.send("This is not an NSFW channel.", ephemeral=True)
            return

        if not tags:
            await ctx.send("Please provide at least one tag.", ephemeral=True)
            return

        r34Py = rule34Py()
        result_random = r34Py.random_post([tags])

        if result_random:
            embed = disnake.Embed()
            embed.set_image(url=str(result_random.image))
            await ctx.send(embed=embed)
        else:
            await ctx.send("No results found for the provided tags.", ephemeral=True)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('!картинка '):
            query = message.content[9:]

            translator = Translator(to_lang="en", from_lang="ru")
            translated_query = translator.translate(query)

            headers = {
                "Authorization": f"Client-ID {UNSPLASH_API_KEY}",
            }
            params = {
                "query": translated_query,  
            }

            try:
                response = requests.get(UNSPLASH_API, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    if "results" in data and data["results"]:
                        chosen_image = random.choice(data["results"])
                        image_url = chosen_image["urls"]["regular"]

                        embed = disnake.Embed()
                        embed.set_image(url=image_url)

                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("Ничего не найдено.")
                else:
                    await message.channel.send("Ошибка при выполнении запроса к Unsplash API.")

            except Exception as e:
                await message.channel.send(f"Произошла ошибка: {e}")
    
def setup(client):
    client.add_cog(Commands(client))