import discord
from discord.ext import commands
from discord import option

#請創建名為data資料夾

cid=1048577759183642646
#此為 當有訊息就創建

class yn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="贊成",
        style=discord.ButtonStyle.green,
        custom_id="awa:yes",
    )
    async def green(self, button: discord.ui.Button, interaction: discord.Interaction):
        with open(f"data/{interaction.message.id}-yes.txt", 'r') as filt:
            y=filt.read()
        with open(f"data/{interaction.message.id}-no.txt", 'r') as filt:
            n=filt.read()
        if str(interaction.user.id) in y:
            await interaction.response.send_message("你已經投給`贊成`過了", ephemeral=True)
            return
        elif str(interaction.user.id) in n:
            await interaction.response.send_message("你已經投給`不贊成`過了", ephemeral=True)
            return
        else:
            with open(f"data/{interaction.message.id}-yes.txt", 'a') as filt:
                filt.write(f"{interaction.user.id}\n")
            await interaction.response.send_message("你成功投給`贊成`", ephemeral=True)


    @discord.ui.button(
        label="不贊成", style=discord.ButtonStyle.red, custom_id="awa:no"
    )
    async def red(self, button: discord.ui.Button, interaction: discord.Interaction):
        with open(f"data/{interaction.message.id}-yes.txt", 'r') as filt:
            y=filt.read()
        with open(f"data/{interaction.message.id}-no.txt", 'r') as filt:
            n=filt.read()
        if str(interaction.user.id) in y:
            await interaction.response.send_message("你已經投給`贊成`過了", ephemeral=True)
            return
        elif str(interaction.user.id) in n:
            await interaction.response.send_message("你已經投給`不贊成`過了", ephemeral=True)
            return
        else:
            with open(f"data/{interaction.message.id}-no.txt", 'a') as filt:
                filt.write(f"{interaction.user.id}\n")
            await interaction.response.send_message("你成功投給`不贊成`", ephemeral=True)


    @discord.ui.button(
        label="誰投票了?", style=discord.ButtonStyle.grey, custom_id="awa:who"
    )
    async def grey(self, button: discord.ui.Button, interaction: discord.Interaction):
        yl = len(open(f"data/{interaction.message.id}-yes.txt",'rU').readlines())
        nl = len(open(f"data/{interaction.message.id}-no.txt",'rU').readlines())
        embed = discord.Embed(title="以下是統計數據")
        embed.add_field(name=f"贊成", value=f"共{yl}人")
        embed.add_field(name=f"不贊成", value=f"共{nl}人")
        #
        await interaction.response.send_message(content=None, embed=embed, ephemeral=True)




class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),intents=discord.Intents.all()
        )
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(yn())
            self.persistent_views_added = True

        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
bot=PersistentViewBot()


@bot.slash_command(description="開始投票")
@option("text", description="輸入要投票的項目")
async def 投票(ctx,text:str):
    embed = discord.Embed(title="你是否贊成:", description=f"```\n{text}\n```", color=0x04f108)
    embed.set_footer(text=f"發起人: {ctx.author}")
    i = await ctx.respond(content=None, embed=embed, view=yn())
    with open(f"data/{i.id}-yes.txt", 'a') as filt:
        pass
    with open(f"data/{i.id}-no.txt", 'a') as filt:
        pass
    print(i)


@bot.event
async def on_message(msg):
    if msg.author.id == bot.user.id:
        return
    if msg.channel.id == cid:
        await msg.delete()
        embed = discord.Embed(title="你是否贊成:", description=f"```\n{msg.content}\n```", color=0x04f108)
        embed.set_footer(text=f"發起人: {msg.author}")
        i = await msg.channel.send(content=None, embed=embed, view=yn())
        with open(f"data/{i.id}-yes.txt", 'a') as filt:
            pass
        with open(f"data/{i.id}-no.txt", 'a') as filt:
            pass
        print(i)

@bot.slash_command(description="回復建議")
@commands.has_permissions(manage_messages=True)
@option("id", description="輸入要回復的訊息id")
@option("text", description="輸入要回復的訊息文字")
async def 回復(ctx,id:str,text:str):
    msg = await ctx.fetch_message(int(id))
    print(msg)
    await msg.edit(f"回復: {text} ||最後編輯:{ctx.author}||")
    await ctx.respond(f"反應成功!!\nhttps://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{id}", ephemeral=True)
    
bot.run("token")
