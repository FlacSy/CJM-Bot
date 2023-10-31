import disnake
from disnake.ext import commands



class FunctionalMenu(disnake.ui.Select):
    def __init__(self):
        selectOptions = [
            disnake.SelectOption(label='◦ Кастомизация', value='customization_menu'),
            disnake.SelectOption(label='◦ Функионал бота', value='help_server_menu')
        ]
        super().__init__(placeholder='⑆ Функионал', options=selectOptions)

class HelpServerMenu(disnake.ui.Select):
    def __init__(self):
        select_options = [
            disnake.SelectOption(label='⭒ Игры', value='help_server_menu_game'),
            disnake.SelectOption(label='⭒ Боты', value='help_server_menu_bots'),
            disnake.SelectOption(label='⭒ Связь с администрацией', value='help_server_menu_admin_conect'),
        ]
        super().__init__(placeholder='Помощь по серверу', options=select_options)

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''-------------------Обробочик событий-------------------'''
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')

    '''-------------------Обробочик выбора-------------------'''
    @commands.Cog.listener()
    async def on_dropdown(self, inter: disnake.MessageInteraction):
        user = inter.user
        role = disnake.utils.get(user.roles, name="bump")
        guild = inter.guild 
        '''-------------------Меню с бампами-------------------'''
        if 'participation_bump_true' in inter.values:
            if role is None:
                role = disnake.utils.get(inter.guild.roles, name="bump")
                if role:
                    embed = disnake.Embed(title="Теперь вы участвуете в бампах 😊", color=0x57FF6A)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/1153144293247176724/1154498688262082682/15_s.jpg")
                    await inter.response.send_message(embed = embed, ephemeral=True)
                    await user.add_roles(role)
                else:
                    await inter.response.send_message("Роль не найдена.", ephemeral=True)

def setup(bot):
    bot.add_cog(Info(bot))