import json
import time
import requests
from datetime import datetime, timedelta
import copy
import discord
from discord.ext import commands
from discord.ext import tasks
import schedule
import string


class Edupage(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.update.start()

        self.schedule_time = datetime.strptime("2020-11-10 7:00:00", '%Y-%m-%d %H:%M:%S')
        while self.schedule_time <= datetime.now():
            self.schedule_time += timedelta(hours=12)
        # self.schedule_time += timedelta(hours=-12)    #  turn this on to show deadlines on bot reset

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mess(self, ctx, amount=1):
        try:
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

            # going over edu
            messages = edu['timelineItems']
            to_show = []

            for message in messages:
                if message["typ"] == "sprava":
                    to_show.append(message)

            # going over edu0
            to_show0 = []
            if no_edu0 is False:
                messages = edu0['timelineItems']

                for message in messages:
                    if message["typ"] == "sprava":
                        to_show0.append(message)

            # going over edu1
            to_show1 = []
            if no_edu1 is False:
                messages = edu1['timelineItems']

                for message in messages:
                    if message["typ"] == "sprava":
                        to_show1.append(message)

            # cutting the files to required size
            while len(to_show) > int(amount):
                del to_show[-1]

            if no_edu0 is False:
                while len(to_show0) > int(amount):
                    del to_show0[-1]

            if no_edu1 is False:
                while len(to_show1) > int(amount):
                    del to_show1[-1]

            # merging them together
            merged = merge(to_show, to_show0, to_show1)

            while len(merged) > int(amount):
                del merged[-1]

            # displaying
            for message in merged:
                try:
                    await ctx.send(f"```{message['cas_pridania']}       {message['user_meno']}\n"
                                   f"{message['vlastnik_meno']}: {message['text']}```")
                except:
                    mess = discord.Embed(title="Message",
                                         description=f"{message['user_meno']}")
                    mess.add_field(name=f"{message['vlastnik_meno']}:",
                                   value=f"text way to long, will be displayed as string")
                    await ctx.send(content=None, embed=mess)

                    # copying code from another bot i made
                    message_content = message["text"].split("\n")
                    lengths = list(map(len, message_content))

                    cur_length = lengths[0]
                    low = 0
                    for i in range(1, len(lengths)):
                        if cur_length + lengths[i] > 1700:  # space for 204 \n
                            send_string = '\n'.join(message_content[low:i])
                            try:
                                await ctx.send(f"```{send_string}```")
                            except:
                                pass
                            low = i
                            cur_length = 0
                        cur_length += lengths[i]
        except Exception as e:
            with open("/home/dietpi/Edu-kun_v.2.0/saves/error_log.txt", "w+") as f:
                f.write(str(e))
                f.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def homework(self, ctx, amount=1):
        try:
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

            # going over edu
            messages = edu['homeworks']
            to_show = []

            for message in messages:
                to_show.append(message)

            # going over edu0
            to_show0 = []
            if no_edu0 is False:
                messages = edu0['homeworks']

                for message in messages:
                    to_show0.append(message)

            # going over edu1
            to_show1 = []
            if no_edu1 is False:
                messages = edu1['homeworks']

                for message in messages:
                    to_show1.append(message)

            # cutting the files to required size
            while len(to_show) > int(amount):
                del to_show[-1]

            if no_edu0 is False:
                while len(to_show0) > int(amount):
                    del to_show0[-1]

            if no_edu1 is False:
                while len(to_show1) > int(amount):
                    del to_show1[-1]

            # merging them together
            merged = merge(to_show, to_show0, to_show1)

            while len(merged) > int(amount):
                del merged[-1]

            for message in merged:
                try:
                    await ctx.send(f"```{message['datecreated']}       {message['autor_meno']}\n"
                                   f"predmet:   {message['predmet_meno']}:\n"
                                   f"text:      {message['name']}\n"
                                   f"deadline:  {message['datetimeto']}```")
                except:
                    await ctx.send(f"```{message['datecreated']}       {message['autor_meno']}\n"
                                   f"predmet:   {message['predmet_meno']}:\n"
                                   f"text:      {message['name']}\n"
                                   f"deadline:  {message['dateto']}```")
        except Exception as e:
            with open("/home/dietpi/Edu-kun_v.2.0/saves/error_log.txt", "w+") as f:
                f.write(str(e))
                f.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def new(self, ctx):  # not always context cause automation sometimes only channel is passed
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

        # merged = merge(to_show, to_show0, to_show1)
        merged = to_show1 + to_show0 + to_show

        # displaying
        if merged:
            for message in merged:
                try:
                    homework = discord.Embed(title=f"Homework",
                                             description=f"{message['datecreated']} - {message['autor_meno']}")
                    homework.add_field(name=f"Subject:",
                                       value=f"{message['predmet_meno']}")
                    homework.add_field(name=f"Text:",
                                       value=f"{message['name']}")
                    homework.add_field(name=f"Deadline:",
                                       value=f"{message['datetimeto']}")
                    await ctx.send(content=None, embed=homework)
                except:
                    homework = discord.Embed(title=f"Homework",
                                             description=f"{message['datecreated']} - {message['autor_meno']}")
                    homework.add_field(name=f"Subject:",
                                       value=f"{message['predmet_meno']}")
                    homework.add_field(name=f"Text:",
                                       value=f"{message['name']}")
                    homework.add_field(name=f"Deadline:",
                                       value=f"{message['dateto']}")
                    await ctx.send(content=None, embed=homework)

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

        # getting names to filter from database

        with open("/home/dietpi/Edu-kun_v.2.0/saves/names.json", "r") as f:
            namesX = json.load(f)

        try:
            names += namesX[str(ctx.guild.id)]
        except:
            pass

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

        # merged = merge(to_show, to_show0, to_show1)
        merged = to_show1 + to_show0 + to_show

        # displaying
        if merged:
            for message in merged:
                try:
                    mess = discord.Embed(title="Message",
                                         description=f"{message['user_meno']}")
                    mess.add_field(name=f"{message['vlastnik_meno']}:",
                                   value=f"{message['text']}")
                    await ctx.send(content=None, embed=mess)
                except:
                    mess = discord.Embed(title="Message",
                                         description=f"{message['user_meno']}")
                    mess.add_field(name=f"{message['vlastnik_meno']}:",
                                   value=f"text way to long, will be displayed as string")
                    await ctx.send(content=None, embed=mess)

                    # copying code from another bot i made
                    message_content = message["text"].split("\n")
                    lengths = list(map(len, message_content))

                    if sum(lengths) <= 1700:
                        await ctx.send(f"```{message['text']}```")

                    cur_length = lengths[0]
                    low = 0
                    for i in range(1, len(lengths)):
                        if cur_length + lengths[i] > 1700:  # space for 204 \n
                            send_string = '\n'.join(message_content[low:i])
                            try:
                                await ctx.send(f"```{send_string}```")
                            except:
                                pass
                            low = i
                            cur_length = 0
                        cur_length += lengths[i]

        # appending new messages to old ones
        for iD in new_e_superids:
            old["homework"][iD] = iD
        for iD in new_timelineids:
            old["messages"][iD] = iD

        oldMain[str(ctx.guild.id)] = old

        with open("/home/dietpi/Edu-kun_v.2.0/saves/old.json", "w") as f:
            json.dump(oldMain, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def deadline(self, ctx):
        try:

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

            edu = edu["homeworks"]
            if no_edu0 is False:
                edu0 = edu0["homeworks"]
            else:
                edu0 = []

            if no_edu1 is False:
                edu1 = edu1["homeworks"]
            else:
                edu1 = []

            merged = merge(edu, edu0, edu1)
            for message in merged:
                try:
                    x = datetime.strptime(message["datetimeto"], '%Y-%m-%d %H:%M:%S')
                except:
                    x = datetime.strptime(message["dateto"], '%Y-%m-%d')
                if datetime.now() + timedelta(days=1) > x > datetime.now():
                    try:
                        homework = discord.Embed(title=f"!!!DEADLINE!!!",
                                                 description=f"{message['datecreated']} - {message['autor_meno']}")
                        homework.add_field(name=f"Subject:",
                                           value=f"{message['predmet_meno']}")
                        homework.add_field(name=f"Text:",
                                           value=f"{message['name']}")
                        homework.add_field(name=f"Deadline:",
                                           value=f"{message['datetimeto']}")
                        await ctx.send(content=None, embed=homework)
                    except:
                        homework = discord.Embed(title="!!!DEADLINE!!!",
                                                 description=f"{message['datecreated']} - {message['autor_meno']}")
                        homework.add_field(name=f"Subject:",
                                           value=f"{message['predmet_meno']}")
                        homework.add_field(name=f"Text:",
                                           value=f"{message['name']}")
                        homework.add_field(name=f"Deadline:",
                                           value=f"{message['dateto']}")
                        await ctx.send(content=None, embed=homework)
        except Exception as e:
            with open("/home/dietpi/Edu-kun_v.2.0/saves/error_log.txt", "w+") as f:
                f.write(str(e))
                f.close()

    @tasks.loop(seconds=120.0)
    async def update(self):
        print("time for cycle")
        with open("/home/dietpi/Edu-kun_v.2.0/saves/setup.json", "r") as f:
            setupX = json.load(f)

        try:
            with open("/home/dietpi/Edu-kun_v.2.0/saves/channels.json", "r") as f:
                channels = json.load(f)

            for server in self.client.guilds:
                try:
                    for channel in server.channels:
                        if channel.name == channels[str(server.id)]:
                            await self.new(channel)
                except Exception as e:
                    if setupX[str(server.id)]['debug']:
                        await server.channels[-1].send("A problem has occurred.")
                        with open("/home/dietpi/Edu-kun_v.2.0/saves/error_log.txt", "w+") as f:
                            f.write(str(e))
                            f.close()

            now = datetime.now()
            if self.schedule_time <= now:
                for server in self.client.guilds:
                    try:
                        for channel in server.channels:
                            if channel.name == channels[str(server.id)]:
                                await self.deadline(channel)
                    except:
                        if setupX[str(server.id)]['debug']:
                            await server.channels[-1].send("A problem has occurred.")
                self.schedule_time += timedelta(hours=12)
        except Exception as e:
            with open("/home/dietpi/Edu-kun_v.2.0/saves/error_log.txt", "w+") as f:
                f.write(str(e))
                f.close()


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
                if values['username'] == "JakubDuris":
                    pass
                edupage = requests.session()
                edupage.post(url, data=values, headers=headers)
                r = edupage.get("https://spspb.edupage.org/timeline/", headers=headers)
                x = r.text.split("\n")
                lines_to_del = []
                if values['username'] == "JakubDuris":
                    pass
                for line in x:
                    if len(line) < 10000:
                        lines_to_del.append(line)

                for line in lines_to_del:
                    del x[x.index(line)]
                if values['username'] == "JakubDuris":
                    pass

                x = list(x[0])
                while x[0] != "{":
                    del x[0]
                while x[-1] != "}":
                    del x[-1]
                x = "".join(x)
                x = x.replace("false", "False").replace("true", "True").replace("null", "None")
                var = eval(x)

                if values['username'] == "JakubDuris":
                    pass
                with open(f"/home/dietpi/Edu-kun_v.2.0/saves/{accounts[account]['file']}", "r") as f:
                    save = json.load(f)

                save[str(ctx.guild.id)] = var

                with open(f"/home/dietpi/Edu-kun_v.2.0/saves/{accounts[account]['file']}", "w") as f:
                    json.dump(save, f, indent=4)
                break
            except Exception as e:
                time.sleep(0.5)
                print(accounts[account]['name'])
                print(str(e))


def merge(list0, list1, *args):

    try:
        if list0[0]['typ'] == "sprava":
            l0 = [[datetime.strptime(item['cas_pridania'], '%Y-%m-%d %H:%M:%S'), item] for item in list0]
            l1 = [[datetime.strptime(item['cas_pridania'], '%Y-%m-%d %H:%M:%S'), item] for item in list1]
        else:
            raise Exception
    except:
        l0 = [[datetime.strptime(item['datecreated'], '%Y-%m-%d %H:%M:%S'), item] for item in list0]
        l1 = [[datetime.strptime(item['datecreated'], '%Y-%m-%d %H:%M:%S'), item] for item in list1]

    l2 = l0 + l1
    merged = copy.deepcopy(l2)

    # remove duplicates

    merged = unduplicate(merged)

    skip = False
    if len(merged) < 2:
        skip = True

    if skip is False:
        for i in range(1, len(merged)):
            while merged[i][0] < merged[i-1][0] and i > 0:
                c = merged[i]
                merged[i] = merged[i-1]
                merged[i-1] = c
                i -= 1

    merged.reverse()
    merged = [item[1] for item in merged]

    if len(args) > 0:
        for li in args:
            merged = merge(merged, li)

    return merged


def unduplicate(listX):
    for item in listX:
        l3 = copy.copy(listX)
        l3.remove(item)

        for itemX in l3:
            if item[0] == itemX[0]:
                listX = unduplicate(l3)
                return listX
    return listX


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
    client.add_cog(Edupage(client))
