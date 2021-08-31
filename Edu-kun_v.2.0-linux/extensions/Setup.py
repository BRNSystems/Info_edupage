import json
import string
import time
import requests
import discord
from discord.ext import commands


class Setup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_client(self, ctx, name, password, save_number_0_1_2):
        with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "r") as f:
            accounts = json.load(f)

        save_num = int(save_number_0_1_2)-1
        if save_num == -1:
            save_num = ""

        server_accounts = accounts[str(ctx.guild.id)]

        server_accounts[name] = {"name": name,
                                 "password": weird_shuffle(password),
                                 "file": f"edu{save_num}.json"}

        accounts[str(ctx.guild.id)] = server_accounts

        await ctx.channel.purge(limit=1)

        await ctx.send(f"Client for account {name} added.")

        with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "w") as f:
            json.dump(accounts, f, indent=4)

        await self.h_m(ctx)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_clients(self, ctx):
        with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "r") as f:
            accounts = json.load(f)

        accounts[str(ctx.guild.id)] = {}

        await ctx.send("Cleared clients.")

        with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "w") as f:
            json.dump(accounts, f, indent=4)

        # removing accounts
        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "r") as f:
            save = json.load(f)

        save[str(ctx.guild.id)] = {}

        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "w") as f:
            json.dump(save, f, indent=4)

        # removing accounts
        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu0.json", "r") as f:
            save = json.load(f)

        save[str(ctx.guild.id)] = {}

        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu0.json", "w") as f:
            json.dump(save, f, indent=4)

        # removing accounts
        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu1.json", "r") as f:
            save = json.load(f)

        save[str(ctx.guild.id)] = {}

        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu1.json", "w") as f:
            json.dump(save, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx, channel_name):
        with open("/home/dietpi/Edu-kun_v.2.0/saves/channels.json", "r") as f:
            channels = json.load(f)

        channels[str(ctx.guild.id)] = channel_name

        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                await channel.send("This channel is now set as the channel where bot sends messages(notifications).\n"
                                   f"<@{ctx.author.id}>")

        with open("/home/dietpi/Edu-kun_v.2.0/saves/channels.json", "w") as f:
            json.dump(channels, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def debug(self, ctx, True_False):
        if True_False in ["True", "true"]:

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
                setupX = json.load(f)

            setupX[str(ctx.guild.id)]['debug'] = True

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "w") as f:
                json.dump(setupX, f, indent=4)

            await ctx.send("Debug is now on.")
        elif True_False in ["False", "false"]:

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
                setupX = json.load(f)

            setupX[str(ctx.guild.id)]['debug'] = False

            with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "w") as f:
                json.dump(setupX, f, indent=4)

            await ctx.send("Debug is now off.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def h_m(self, ctx):
        update_database(ctx)

        no_edu0 = False
        no_edu1 = False

        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "r") as f:
            edu = json.load(f)
            edu = edu[str(ctx.guild.id)]
        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu0.json", "r") as f:
            try:
                edu0 = json.load(f)
                edu0 = edu0[str(ctx.guild.id)]
                if len(edu0.keys()) == 0:
                    raise Exception("nothing inside")
            except:
                no_edu0 = True
        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu1.json", "r") as f:
            try:
                edu1 = json.load(f)
                edu1 = edu1[str(ctx.guild.id)]
                if len(edu1.keys()) == 0:
                    raise Exception("nothing inside")
            except:
                no_edu1 = True

        with open("/home/dietpi/Edu-kun_v.2.0/saves/old.json", "r") as f:
            oldMain = json.load(f)

        old = oldMain[str(ctx.guild.id)]

        new_e_superids = []
        new_timelineids = []

        # handling homework
        messages = edu['homeworks']
        to_show = []
        for message in messages:
            try:
                if message["e_superid"] not in old["homework"].keys():
                    to_show.append(message)
                    new_e_superids.append(message["e_superid"])
                else:
                    pass
            except:
                pass

        to_show0 = []
        if no_edu0 is False:
            messages = edu0['homeworks']
            for message in messages:
                try:
                    if message["e_superid"] not in old["homework"].keys():
                        if message["e_superid"] not in new_e_superids:
                            new_e_superids.append(message["e_superid"])
                            to_show0.append(message)
                    else:
                        pass
                except:
                    pass

        to_show1 = []
        if no_edu1 is False:
            messages = edu1['homeworks']
            for message in messages:
                try:
                    if message["e_superid"] not in old["homework"].keys():
                        if message["e_superid"] not in new_e_superids:
                            new_e_superids.append(message["e_superid"])
                            to_show1.append(message)
                    else:
                        pass
                except:
                    pass

        # handling messages
        # getting client names to remove private messages

        with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json", "r") as f:
            accounts = json.load(f)
            accounts = accounts[str(ctx.guild.id)]

        names = [accounts[x]["name"] for x in accounts.keys()]

        for name in range(len(names)):
            i = 0
            li = 0
            for char in names[name]:
                if char in string.ascii_uppercase:
                    i += 1
                    if i == 2:
                        names[name] = f"{names[name][:li]} {names[name][li:]}"
                li += 1

        # looking for messages
        to_show = []
        messages = edu["timelineItems"]
        for message in messages:
            if message["timelineid"] not in old['messages'].keys():
                if message['typ'] == "sprava":
                    if message["user_meno"] not in names:
                        to_show.append(message)
                        new_timelineids.append(message["timelineid"])
            else:
                pass

        to_show0 = []
        if no_edu0 is False:
            messages = edu0["timelineItems"]
            for message in messages:
                if message["timelineid"] not in old['messages'].keys():
                    if message["timelineid"] not in new_timelineids:
                        if message['typ'] == "sprava":
                            if message["user_meno"] not in names:
                                to_show0.append(message)
                                new_timelineids.append(message["timelineid"])
                else:
                    pass

        to_show1 = []
        if no_edu1 is False:
            messages = edu1["timelineItems"]
            for message in messages:
                if message["timelineid"] not in old['messages'].keys():
                    if message["timelineid"] not in new_timelineids:
                        if message['typ'] == "sprava":
                            if message["user_meno"] not in names:
                                to_show1.append(message)
                                new_timelineids.append(message["timelineid"])
                else:
                    pass

        # appending new messages to old ones
        for iD in new_e_superids:
            old["homework"][iD] = iD
        for iD in new_timelineids:
            old["messages"][iD] = iD

        oldMain[str(ctx.guild.id)] = old

        with open("/home/dietpi/Edu-kun_v.2.0/saves/old.json", "w") as f:
            json.dump(oldMain, f, indent=4)

        await ctx.send("Done")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def filter_name(self, ctx, *, name):
        with open("/home/dietpi/Edu-kun_v.2.0/saves/names.json", "r") as f:
            names = json.load(f)

        try:
            names[str(ctx.guild.id)]
        except Exception as e:
            names[str(ctx.guild.id)] = []

        names[str(ctx.guild.id)].append(str(name))

        with open("/home/dietpi/Edu-kun_v.2.0/saves/names.json", "w") as f:
            json.dump(names, f, indent=4)

        await ctx.send(f"Name {name} added to filter.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_filter(self, ctx):
        with open("/home/dietpi/Edu-kun_v.2.0/saves/names.json", "r") as f:
            names = json.load(f)

        names.pop(str(ctx.guild.id))

        with open("/home/dietpi/Edu-kun_v.2.0/saves/names.json", "w") as f:
            json.dump(names, f, indent=4)

        await ctx.send("Filter cleared.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def HOW_TO_SETUP(self, ctx):
        tutorial = discord.Embed(title="Tutorial")

        tutorial.add_field(name="1. setting channel",
                           value="use &set_channel <channel-name> to set channel where bot should send notifications.")
        tutorial.add_field(name="2. adding clients",
                           value="use &add_client <username-on-edupage> <password-on-edupage> <number of save>\n"
                           "Number of save can be either 0, 1 or 2, one save can have maximum of 1 account.\n"
                           "If something isnt working u can use &clear_clients to reset.")
        tutorial.add_field(name="3. filtering",
                           value="This is for special cases, normally personal messages are filtered automatically"
                           " using edupage username but in some cases edupage uses different name than username"
                           "for messages. \nTo fix this we use &filter_name <name_to_filter> that filters private "
                           "messages with that name, parameter <name_to_filter> can contain spaces.\n"
                           "If you made a mistake u can use &clear_filter to reset filtered names.")
        tutorial.add_field(name="4. not working",
                           value="If bot starts spamming messages and isnt stopping(this shouldnt happen)\n"
                           "try using &h_m.\n"
                           "Lastly theres &debug <true/false>, use this if u want to know if bot is dead or u did"
                           " a mistake while adding clients, if u did a mistake it should start sending message "
                           "'A problem has occurred' somewhere.")
        await ctx.send(content=None, embed=tutorial)


def update_database(ctx):
    # getting accounts
    with open("/home/dietpi/Edu-kun_v.2.0/saves/accounts.json") as f:
        accounts = json.load(f)[str(ctx.guild.id)]

    for account in accounts.keys():
        for i in range(6):
            try:
                url = 'https://spspb.edupage.org/login/edubarLogin.php'
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"}
                values = {'username': f"{accounts[account]['name']}",
                          'password': f"{weird_shuffle(accounts[account]['password'])}"}
                edupage = requests.session()
                edupage.post(url, data=values, headers=headers)
                r = edupage.get("https://spspb.edupage.org/timeline/", headers=headers)
                x = r.text.split("\n")
                lines_to_del = []
                for line in x:
                    if len(line) < 10000:
                        lines_to_del.append(line)

                for line in lines_to_del:
                    del x[x.index(line)]

                x = list(x[0])
                while x[0] != "{":
                    del x[0]
                while x[-1] != "}":
                    del x[-1]
                x = "".join(x)
                x = x.replace("false", "False").replace("true", "True").replace("null", "None")
                var = eval(x)

                with open(f"/home/dietpi/Edu-kun_v.2.0/saves/{accounts[account]['file']}", "r") as f:
                    save = json.load(f)

                save[str(ctx.guild.id)] = var

                with open(f"/home/dietpi/Edu-kun_v.2.0/saves/{accounts[account]['file']}", "w") as f:
                    json.dump(save, f, indent=4)
                break
            except:
                time.sleep(0.5)


def weird_shuffle(message):
    x = message
    o = []
    e = []
    ind = []
    gug = 0
    for i in x:
        o.append(i)
    f = len(x) / 2
    if f % 1 == 0:
        o.append(" ")
        gug = 1
    p = len(o)
    for u in range(0, p):
        ind.append(u)
    for ef in range(0, p):
        if max(ind) - ef * 2 < 0:
            break
        e.append(o[max(ind) - ef * 2])
        if min(ind) + 1 + (ef * 2) > max(ind):
            break
        e.append(o[min(ind) + 1 + (ef * 2)])
    zet = ["", p]
    if gug == 1:
        e.remove(e[0])
        zet[0] = " "
        zet[1] = p - 1
    gug = ""
    for ups in range(0, zet[1]):
        gug += e[ups]
    return zet[0] + gug


def setup(client):
    client.add_cog(Setup(client))
