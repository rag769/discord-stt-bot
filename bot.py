import config
import discord
from discord.ext import commands
import stt

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

@bot.event
async def setup_hook():
    await bot.add_cog(stt.SpeechToText(bot, config.WIT_TOKEN))

bot.run(config.DISCORD_TOKEN)
