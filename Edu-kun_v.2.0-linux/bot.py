import discord
import random
import json
import os
from discord.ext import commands
from discord.ext import tasks


intents = discord.Intents.default()
intents.members = True


def get_prefix(clientX, message):
    with open("/home/dietpi/Edu-kun_v.2.0/saves/prefixes", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix, intents=intents)


@client.event
async def on_ready():
    print("Edu is ready.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Awake"))


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, *, extension="all"):
    if str(extension) not in ["all", "All"]:
        client.load_extension(f"extensions.{extension}")
        await ctx.send(f"Reloaded extension {extension}.")
    else:
        try:
            for ext in os.listdir("extensions"):
                if ext.endswith(".py"):
                    try:
                        client.load_extension(f"extensions.{ext[:-3]}")
                    except:
                        pass
            await ctx.send(f"Reloaded all extensions successfully.")
        except:
            await ctx.send("Error")


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, *, extension="all"):
    if str(extension) not in ["all", "All"]:
        client.unload_extension(f"extensions.{extension}")
        await ctx.send(f"Reloaded extension {extension}.")
    else:
        try:
            for ext in os.listdir("extensions"):
                if ext.endswith(".py"):
                    try:
                        client.unload_extension(f"extensions.{ext[:-3]}")
                    except:
                        pass
            await ctx.send(f"Reloaded all extensions successfully.")
        except:
            await ctx.send("Error")


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, *, extension="all"):
    if str(extension) not in ["all", "All"]:
        try:
            client.unload_extension(f"extensions.{extension}")
            client.load_extension(f"extensions.{extension}")
            await ctx.send(f"Reloaded extension {extension}.")
        except Exception as e:
            with open("/home/dietpi/Edu-kun_v.2.0/saves/error_log.txt", "w+") as f:
                f.write(str(e))
                f.close()
            await ctx.send("Error")
    else:
        try:
            for ext in os.listdir("extensions"):
                if ext.endswith(".py"):
                    try:
                        client.unload_extension(f"extensions.{ext[:-3]}")
                    except:
                        pass
                    client.load_extension(f"extensions.{ext[:-3]}")
            await ctx.send(f"Reloaded all extensions successfully.")
        except Exception as e:
            with open("/home/dietpi/Edu-kun_v.2.0/saves/error_log.txt", "w+") as f:
                f.write(str(e))
                f.close()
            await ctx.send("Error")


for ext in os.listdir("extensions"):
    if ext.endswith(".py"):
        client.load_extension(f"extensions.{ext[:-3]}")


client.run("ID")
