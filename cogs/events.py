import discord
from discord.ext import commands

async def update_activity(client):
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | ?help"))
    print("Updated presence")

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        cha = self.client.get_channel(925513395883606129)
        await cha.send(embed=discord.Embed(title="Join", description=f"Joined: {guild.name}"))

        await update_activity(self.client)

        embed = discord.Embed(color=discord.Color(value=0x36393e))
        embed.set_author(name="I am a captcha bot:")
        embed.add_field(name="This is a very simple bot",value="First you use `-setrole @[VerifiedRole]` and then you can do `-captcha` and it will make the button for them to verify\nThe verified role is the role they will get once they complete the captcha")
        embed.set_footer(text=f"Thank You - Captcha Bot is now on {len(self.client.guilds)} servers!")
        try:
            await guild.system_channel.send(content="**Thanks for inviting me! :wave: **", embed=embed)
        except Exception as e:
            for i in guild.channels:
                try:
                    i.send(content="**Thanks for inviting me! :wave: **", embed=embed)
                    break
                except:
                    pass
                    

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await update_activity(self.client)
        cha = self.client.get_channel(925513395883606129)
        await cha.send(embed=discord.Embed(title="Leave", description=f"Left: {guild.name}"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass

def setup(client):
    client.add_cog(Events(client))