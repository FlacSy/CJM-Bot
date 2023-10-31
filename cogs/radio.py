import disnake
from disnake import FFmpegPCMAudio, Activity, ActivityType
from disnake.ext import commands
import asyncio
import sqlite3
from main import conn, cursor

cursor.execute('''CREATE TABLE IF NOT EXISTS radio_channel (
                  server_id INTEGER PRIMARY KEY,
                  channel_id INTEGER
               )''')

conn.commit()

class Radio(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn
        self.radio_themes = [
            'http://stream.radioparadise.com/',
            'https://fluxfm.streamabc.net/flx-chillhop-mp3-128-8581707?sABC=6509rr0s%230%2313812os2n1nrrr3qr45580n9807sss54%23fgernzf.syhksz.qr&aw_0_1st.playerid:streams.fluxfm.de&amsparams:playerid:streams.fluxfm.de;skey:1695149583',
            'http://stream.radioparadise.com/128-rock',
            'https://prod-3-90-240-207.amperwave.net/ppm-jazz24mp3-ibc1?session-id=2f5a71c9d309c4d2774e1892022fd874&source=TuneIn&gdpr=1&us_privacy=1YNY&gdpr_consent=CP0ClYgP0ClYgAcABBENDcCsAP_AAH_AACiQJuhBYC5EDCHBIWJNA9sUOIAEEFQgAGAwCAABACABCBoAIBQA0CAhEAiAACgCAAAAIEAAAAAAAAAABAEAAAAAIACMAACQAAMAIABACAAIAABAAAAAAACREAAAAAAAFAAAkAQAAAIAgEAAFAAAAACgAAAIAKAAAAAAAAAAAAAAEAAAEAgBAEABAAiAAAAAIAAIAAAAAAQAAAAAPXW-9-IKEBsAKQAfgBSgEUAI6ATsBeYDBAGRgMsAeSBBICFQEbwJMAS-gmACYIEwwJigTHAmTBMsEzgJpATUAmxBNsE3AgoAJBICQAFQAOAAgABkADQAIgATAAngBvAEMAI4AUoAtwB3gD9AKeAkQBnwQAKAFAALYA5wGRgPJDABwAhABPgC2ALgApABzgH7AZGGgBAFPAZ8IADABCACeAFsAUgA5wD9iIAQBTwGfCgAoAQgAuACkAGUAfsVABAZ8MABgBCAFIAfsZABAZ8OgNAAVAA4ACAAGQANAAiABMACeAFwAMQAZgA3gCGAFKALcAZQA7wB-gEWAKeAkQBcADLAGfANjAcWOAHgAXACgAFsAL4AaABHACkAHOAO4AhABKgCsgKmAVUA8khAJACYAFwAMQAbwBHADvAKeAuABnxAAMAF8ANAApABzgFZAeSSADAAXAC-AG0AUgA7gCskoBgAHAAiABMAC4AGIAQwAjgBbgDvAKeAkQBnxSAsABUADgAIAAZAA0ACIAEwAJ4AUgAxABmAEMAKUAW4AygB3gD9AIsAkQBcADPgGxlABYAFwAvgBtAEcAKQAc4A7gCsgF1AP-AqYAAA.f_gAD_gAAAAA'
        ]
        self.current_theme_index = 0
        self.theme_names = [
            'Classic Radio',
            'Lofi Music',
            'Rock',
            'Jazz'
        ]

    async def get_next_radio_theme(self):
        theme_music = self.radio_themes[self.current_theme_index]
        self.current_theme_index = (self.current_theme_index + 1) % len(self.radio_themes)
        return theme_music

    def get_current_theme_name(self):
        return self.theme_names[self.current_theme_index]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ког {__name__} загружен...')
        await self.radio_ready()

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def setradiochannel(self, ctx, channel: disnake.StageChannel):
        if ctx.guild:
            server_id = ctx.guild.id
            channel_id = channel.id
            cursor.execute('INSERT OR REPLACE INTO radio_channel (server_id, channel_id) VALUES (?, ?)', (server_id, channel_id))
            self.conn.commit()  # Сохраняем изменения
            await ctx.send(f'Канал радио установлен в {channel.mention}')
            await self.radio_ready()
        else:
            await ctx.send('Вы должны использовать эту команду на сервере Discord.')

    def get_radio_channel(self):
        cursor.execute('SELECT server_id, channel_id FROM radio_channel')
        return cursor.fetchall()

    async def radio_ready(self):
        radio_channel = self.get_radio_channel()

        for server_id, channel_id in radio_channel:
            guild = self.bot.get_guild(server_id)

            if guild is not None:
                bot_speaker = guild.get_member(self.bot.user.id)

                channel = guild.get_channel(channel_id)
                player = await channel.connect()

                while True:
                    theme_music = await self.get_next_radio_theme()
                    theme_name = self.get_current_theme_name()
                    await self.bot.change_presence(status=disnake.Status.online, activity=disnake.Game(name=theme_name))
                    if player.is_playing():
                        player.stop()

                    player.play(FFmpegPCMAudio(theme_music))
                    await bot_speaker.edit(suppress=False)
                    await asyncio.sleep(7200)

    async def check_voice_channel(self, inter: disnake.Integration, theme_music, theme_name):
        voice_channel = self.bot.get_channel()
        try:
            if voice_channel is not None:
                player = voice_channel.guild.voice_client
                if player is not None:
                    player.stop()

                await self.bot.change_presence(status=disnake.Status.online, activity=disnake.Game(name=theme_name))
                player.play(FFmpegPCMAudio(theme_music))
            else:
                await inter.response.send_message("Вы не находитесь в голосовом канале.")
        except Exception as e:
            print(f'Произошла ошибка при воспроизведении музыки: {e}')

def setup(bot):
    bot.add_cog(Radio(bot, conn))
