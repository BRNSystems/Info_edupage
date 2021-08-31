import json
import time
import requests
import discord
from discord.ext import commands


class Edu_Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def teachers(self, ctx):
        update_database(ctx)

        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "r") as f:
            edu = json.load(f)
            edu = edu[str(ctx.guild.id)]

        for teacher in edu["dbi"]["teachers"].keys():
            t = edu['dbi']['teachers'][teacher]
            teacher = discord.Embed(title=f"{t['firstname']} {t['lastname']}",
                                    description="profile")
            teacher.add_field(name="Gender",
                              value=f"{t['gender']}")
            teacher.add_field(name="Started",
                              value=f"{t['datefrom']}")

            await ctx.send(content=None, embed=teacher)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def classes(self, ctx):
        update_database(ctx)

        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "r") as f:
            edu = json.load(f)
            edu = edu[str(ctx.guild.id)]

        for classroom in edu["dbi"]["classes"].keys():
            cr = edu["dbi"]["classes"][classroom]
            teacher_id = cr["teacherid"]
            teach = "None"

            # getting the teacher
            for teacher in edu["dbi"]["teachers"].keys():
                t = edu['dbi']['teachers'][teacher]

                if t["id"] == teacher_id:
                    teach = f"{t['firstname']} {t['lastname']}"

            embed = discord.Embed(title=f"{cr['name']}",
                                  description="info")
            embed.add_field(name="Teacher",
                            value=teach)

            await ctx.send(content=None, embed=embed)

    @commands.command()
    async def periods(self, ctx):
        update_database(ctx)

        with open("/home/dietpi/Edu-kun_v.2.0/saves/edu.json", "r") as f:
            edu = json.load(f)
            edu = edu[str(ctx.guild.id)]

        periods = edu["dbi"]["periods"]

        periodX = discord.Embed(title="Periods",
                                description="hours")

        for period in periods:

            periodX.add_field(name=f"{period['name']}",
                              value=f"{period['starttime']} - {period['endtime']}")

        await ctx.send(content=None, embed=periodX)

    @commands.command()
    async def authors(self, ctx):
        authors = discord.Embed(title="Authors",
                                description="Tucan444, UntriexTv")

        authors.add_field(name="Tucan444",
                          value="https://tucan444.itch.io/")
        authors.add_field(name="UntriexTv",
                          value="https://github.com/UntriexTv")
        await ctx.send(content=None, embed=authors)


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
    client.add_cog(Edu_Info(client))
