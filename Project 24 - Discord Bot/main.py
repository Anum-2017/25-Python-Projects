import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from keep_alive import keep_alive
import random

# Load the bot token from .env file
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Logging to a file
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents)

# Keep the bot alive (for web hosting like Replit)
keep_alive()

# Role used for secret command
secret_role = "Anum"

# When the bot is ready
@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

# Greet new member
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

# Ensure commands work
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# Basic hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

# Assign "Anum" role
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("⚠️ Role doesn't exist. Use `!listroles` to check available roles.")

# Remove "Anum" role
@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("⚠️ Role doesn't exist. Use `!listroles` to check available roles.")

# 🔍 Debugging command to list all roles
@bot.command()
async def listroles(ctx):
    roles = [role.name for role in ctx.guild.roles]
    await ctx.send("Available roles on this server:\n" + "\n".join(roles))

# DM the user
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said: {msg}")

# Reply to message
@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

# Create a poll
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

# Secret command for specific role
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("🎉 Welcome to the Anum bot!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("🚫 You do not have permission to do that!")

# Show user info
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info – {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Display Name", value=member.display_name, inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

# Server information
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Server Info", color=discord.Color.green())
    embed.add_field(name="Server Name", value=guild.name, inline=True)
    embed.add_field(name="Owner", value=guild.owner, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
    await ctx.send(embed=embed)

# Show latency
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 {round(bot.latency * 1000)}ms")

# Say a message
@bot.command()
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

# Clear messages
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Cleared {amount} messages!")
    await msg.delete(delay=3)

# Simple calculator
@bot.command()
async def math(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.send(f"`{expression}` = **{result}**")
    except Exception:
        await ctx.send("❌ Invalid math expression!")

# Tell a random joke
@bot.command()
async def joke(ctx):
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the computer go to therapy? It had too many bytes of issues.",
        "I told my bot a joke, but it didn't get it. Guess it needs more RAM."
    ]
    await ctx.send(random.choice(jokes))

# Start the bot
bot.run(token)
