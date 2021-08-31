import discord
import random
import json
import time
from discord.ext import commands


class Server_Management(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # adding prefix
        with open("/home/dietpi/Edu-kun_v.2.0/saves/prefixes", "r") as f:
            prefixes = json.load(f)

        try:
            prefixes[str(guild.id)]
        except:
            prefixes[str(guild.id)] = "&"

        with open("/home/dietpi/Edu-kun_v.2.0/saves/prefixes", "w") as f:
            json.dump(prefixes, f, indent=4)

        # adding to setup.json

        with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
            setupX = json.load(f)

        try:
            setupX[str(guild.id)]
        except:
            setupX[str(guild.id)] = {"save": False,
                                     "guild_name": guild.name,
                                     "debug": False}

        with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "w") as f:
            json.dump(setupX, f, indent=4)

        # adding accounts

        with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "r") as f:
            accounts = json.load(f)

        try:
            accounts[str(guild.id)]
        except:
            accounts[str(guild.id)] = {}

        with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "w") as f:
            json.dump(accounts, f, indent=4)

        # adding channel

        with open("/home/dietpi/Edu-kun_v.2.0/saves/channels.json", "r") as f:
            channels = json.load(f)

        try:
            channels[str(guild.id)]
        except:
            channels[str(guild.id)] = guild.channels[len(guild.channels)-1].name

            await guild.channels[len(guild.channels)-1].send("This channel has been chosen by Edu-Kun by default "
                                                             "as channel where bot sends messages(notifications)\n"
                                                             "U can change this with command &set_channel "
                                                             "<channel_name>\n "
                                                             "\n\t\tuse &help to get more information")

        with open("/home/dietpi/Edu-kun_v.2.0/saves/channels.json", "w") as f:
            json.dump(channels, f, indent=4)

        # adding to old messages file

        with open("/home/dietpi/Edu-kun_v.2.0/saves/old.json", "r") as f:
            old = json.load(f)

        try:
            old[str(guild.id)]
        except:
            old[str(guild.id)] = {
                "homework": {},
                "messages": {}
            }

        with open("/home/dietpi/Edu-kun_v.2.0/saves/old.json", "w") as f:
            json.dump(old, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        gi = str(guild.id)

        # checking if we want to delete or save the data
        with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
            setupX = json.load(f)

        if setupX[str(guild.id)]["save"] is False:
            # removing prefix
            with open("/home/dietpi/Edu-kun_v.2.0/saves/prefixes", "r") as f:
                prefixes = json.load(f)

            prefixes.pop(gi)

            with open("/home/dietpi/Edu-kun_v.2.0/saves/prefixes", "w") as f:
                json.dump(prefixes, f, indent=4)

            # removing accounts
            with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "r") as f:
                accounts = json.load(f)

            accounts.pop(gi)

            with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "w") as f:
                json.dump(accounts, f, indent=4)

            # removing channel
            with open("/home/dietpi/Edu-kun_v.2.0/saves/channels.json", "r") as f:
                channels = json.load(f)

            channels.pop(gi)

            with open("/home/dietpi/Edu-kun_v.2.0/saves/channels.json", "w") as f:
                json.dump(channels, f, indent=4)

            # removing list of old messages
            with open("/home/dietpi/Edu-kun_v.2.0/saves/old.json", "r") as f:
                old = json.load(f)

            old.pop(gi)

            with open("/home/dietpi/Edu-kun_v.2.0/saves/old.json", "w") as f:
                json.dump(old, f, indent=4)

            try:
                # removing accounts
                with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "r") as f:
                    save = json.load(f)

                save.pop(gi)

                with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "w") as f:
                    json.dump(save, f, indent=4)
            except:
                pass

            try:
                # removing accounts
                with open("/home/dietpi/Edu-kun_v.2.0/saves/edu0.json", "r") as f:
                    save = json.load(f)

                save.pop(gi)

                with open("/home/dietpi/Edu-kun_v.2.0/saves/edu0.json", "w") as f:
                    json.dump(save, f, indent=4)
            except:
                pass

            try:
                # removing accounts
                with open("/home/dietpi/Edu-kun_v.2.0/saves/edu1.json", "r") as f:
                    save = json.load(f)

                save.pop(gi)

                with open("/home/dietpi/Edu-kun_v.2.0/saves/edu1.json", "w") as f:
                    json.dump(save, f, indent=4)
            except:
                pass

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
                setupX = json.load(f)

            setupX.pop(gi)

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "w") as f:
                json.dump(setupX, f, indent=4)

            with open("/home/dietpi/Edu-kun_v.2.0/saves/names.json", "r") as f:
                names = json.load(f)

            try:
                names.pop(gi)
            except:
                pass

            with open("/home/dietpi/Edu-kun_v.2.0/saves/names.json", "w") as f:
                json.dump(names, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

    # server management commands
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, *, prefix):
        with open("/home/dietpi/Edu-kun_v.2.0/saves/prefixes", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("/home/dietpi/Edu-kun_v.2.0/saves/prefixes", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Prefix changed to '{prefix}'.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def save_on_quit(self, ctx, *, bool_):
        if bool_ in ["False", "false", "no", "No"]:

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
                store = json.load(f)

            store[str(ctx.guild.id)]["save"] = False

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "w") as f:
                json.dump(store, f, indent=4)

            await ctx.send("Saving on quit is turned off.")

        elif bool_ in ["True", "true", "yes", "Yes"]:

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
                store = json.load(f)

            store[str(ctx.guild.id)]["save"] = True

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "w") as f:
                json.dump(store, f, indent=4)

            await ctx.send("Saving on quit is turned on.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        amount = int(amount)
        if amount > 1000:
            amount = 1000
        amount += 1
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared {amount - 1} messages.")


def setup(client):
    client.add_cog(Server_Management(client))
