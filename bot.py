import discord
from discord.ext import commands
import os

# Set up bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

@bot.command(name='ping')
async def ping(ctx):
    """Check if bot is responding"""
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.command(name='hello')
async def hello(ctx):
    """Say hello"""
    await ctx.send(f'Hello {ctx.author.mention}! 👋')

@bot.command(name='info')
async def info(ctx):
    """Get bot info"""
    embed = discord.Embed(
        title='Bot Information',
        description='A simple Discord bot hosted on Render!',
        color=discord.Color.blue()
    )
    embed.add_field(name='Servers', value=len(bot.guilds))
    embed.add_field(name='Latency', value=f'{round(bot.latency * 1000)}ms')
    await ctx.send(embed=embed)

# Run the bot
if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print('Error: DISCORD_TOKEN not found in environment variables')
    else:
        bot.run(TOKEN)
