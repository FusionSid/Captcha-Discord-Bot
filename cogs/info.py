import psutil
import discord
from discord.ext import commands
import psutil
import os
import platform

def get_lines():
    lines = 0
    files = []
    for i in os.listdir():
        if i.endswith(".py"):
            files.append(i)
    for i in os.listdir("cogs/"):
        if i.endswith(".py"):
            files.append(f"cogs/{i}")
    for i in files:
        count = 0
        with open(i, 'r') as f:
            for line in f:
                count += 1
        lines += count
    return lines


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite **Captcha Bot** to your server:", description="[Click this link](https://discord.com/api/oauth2/authorize?client_id=940820124556992572&permissions=8&scope=applications.commands%20bot)"))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong!\n{round(self.client.latency * 1000)}ms")

    @commands.command()
    async def info(self, ctx):
        em = discord.Embed(title='Captcha Bot', description='Because you cant trust bots these days')
        em.add_field(inline=False, name="Server Count",value=f"{len(self.client.guilds)}")
        em.add_field(inline=False, name="User Count", value=len(list(self.client.get_all_members())))
        em.add_field(inline=False, name="Ping",value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Mostly made by FusionSid#3645")
        em.add_field(name='CPU Usage',value=f'{psutil.cpu_percent()}%', inline=False)
        em.add_field(name='Memory Usage',value=f'{psutil.virtual_memory().percent}% of ({round((psutil.virtual_memory().total/1073741824), 2)}GB)', inline=False)
        em.add_field(name='Available Memory',value=f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline=False)
        em.add_field(inline=False, name="Python version",value=f"{platform.python_version()}")
        em.add_field(inline=False, name="Running on",value=f"{platform.system()} {platform.release()}")
        em.add_field(name="Python code", value=f"{get_lines()} of code")
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Info(client))
