import discord
import json
from discord.ext import commands
from random_word import RandomWords
from captcha.image import ImageCaptcha
import os

async def gen_captcha(filename):
    word = RandomWords().get_random_word()
    word = str(word)
    word = word.lower()

    image = ImageCaptcha(width=280, height=90)
    image.generate(word)

    image.write(word, filename)

    return word

async def verify_user(client, member, guild):
    word = await gen_captcha(f"./captcha_images/captcha{member.name}.png")
    await member.send(file=discord.File(f"./captcha_images/captcha{member.name}.png"))
    os.remove(f"./captcha_images/captcha{member.name}.png")

    msg = await member.send("Type the word on screen")

    channel = msg.channel
    author = member

    def check(m):
        return m.channel == channel and m.author == author

    answer = await client.wait_for("message", check=check)

    if answer.content.lower() == word:
        with open("./verified.json") as f:
            data = json.load(f)

        data.append(member.id)

        with open("./verified.json", 'w') as f:
            json.dump(data, f, indent=4)

        with open("./roles.json") as f:
            data = json.load(f)
        try:
            role = guild.get_role(data[str(guild.id)])
        except:
            return await member.send("Verification Failed\nRole doesn't exist :(")

        await member.add_roles(role)

        return await member.send("Verified Successfully :)")
        
    else:
        return await member.send("Verification Failed :(\nPress button and verify again")
    

class CaptchaView(discord.ui.View):
    def __init__(self, client, guild):
        super().__init__(timeout=None)
        self.client = client
        self.guild = guild

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def verify(self, button, interaction):
        with open("./verified.json") as f:
            data = json.load(f)
        
        if interaction.user.id in data:
            await interaction.response.send_message("You have already verified", ephemeral=True)

        await interaction.response.send_message("Check your DM's", ephemeral=True)
        await verify_user(self.client, interaction.user, self.guild)


class CapthaBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Makes a button which upon pressing dm's the person a captcha and if they get it right they get a Verified role")
    async def captcha(self, ctx):
        with open("./roles.json") as f:
            data = json.load(f)

        if str(ctx.guild.id) not in data or data[str(ctx.guild.id)] is None:
            return await ctx.send(embed=discord.Embed(title="A verified role has not been set for this server", description="Use `-setrole [@role]` to set it", color=discord.Color.green()))
        else:
            await ctx.send(content="Click to verify", view=CaptchaView(client=self.client, guild=ctx.guild))

    @commands.command(help="Sets the verified role which the user will get once they complete a captcha")
    async def setrole(self, ctx, role:discord.Role):
        with open("./roles.json") as f:
            data = json.load(f)

        data[str(ctx.guild.id)] = role.id

        with open("./roles.json", 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(embed=discord.Embed(title="Verifyed Role has been set to:", description=role.mention, color=discord.Color.green()))

def setup(client):
    client.add_cog(CapthaBot(client))
