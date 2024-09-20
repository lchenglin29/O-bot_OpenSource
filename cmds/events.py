import discord,aiohttp
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data

async def check_wh(channel):
  d = load_json()
  data = d["channel_data"]
  channel_id = str(channel.id)
  if channel_id in data["channel_url"]:
    return str(data["channel_url"][channel_id])
  elif channel_id not in data["channel_url"]:
    webhook = await channel.create_webhook(name='O_bot')
    data["channel_url"].setdefault(channel_id,str(webhook.url))
    d["channel_data"] = data
    write_js(d)
    return str(webhook.url)
    

class event(Cog_Extension):
  @commands.Cog.listener()
  async def on_message(self,message):
    if message.author == self.bot.user:
      return
    elif "痾" in message.content:
      await message.channel.send('痾，蛤')
    elif self.bot.user.mention in message.content:
      await message.channel.send('嗨嗨，需要幫助嗎？')
    else:
      data = load_json()
      try:
        parts = message.content.split(' ',1)
        if parts[0] in data[str(message.author.id)]:
          async with aiohttp.ClientSession() as session:
            webhook_url= await check_wh(message.channel)
            webhook = discord.Webhook.from_url(url=str(webhook_url),session=session)
            await webhook.send(content=parts[1],
            username=data[str(message.author.id)][parts[0]]["name"],
            avatar_url=data[str(message.author.id)][parts[0]]["url"])
            await message.delete()
      except Exception as e:
        print(e)
        
        

  @commands.Cog.listener()
  async def on_member_join(self,member:discord.Member):
    channel = self.bot.get_channel(1202596441088987156)
    if member.guild.id == 1202596440535343154:
      await channel.send(f'{member.mention}，歡迎來到{member.guild.name}！\n你可以看 <#1202599065318326272> 了解O-bot的玩法\n若要開始遊戲，請到 <#1203004488340742214> 使用指令！')

async def setup(bot):
    await bot.add_cog(event(bot))