from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from discord.interactions import Interaction
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data,load_item_data
from typing import Optional
from objects.player_object import players

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

class ctx_cmds(Cog_Extension):

  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.command()
  async def work(self,ctx):
    player = players(str(ctx.author.id))
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可工作',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    money = random.randint(10,100+player.lv*5)
    xp = random.randint(30,100)
    player.change_money(money)
    player.xp += xp
    player.save()
    embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}賺了{money}鎊\nxp+{xp}',color=discord.Color.random())
    await ctx.send(embed=embed)

  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.command()
  async def slut(self,ctx):
    player = players(str(ctx.author.id))
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可使用該指令',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    if player.job != "妓女":
      embed = discord.Embed(title='',description='你又不是妓女',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    money = random.randint(150,250+player.lv*5)
    xp = random.randint(100,150)
    player.change_money(money)
    player.xp += xp
    player.save()
    embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}賺了{money}鎊\nxp+{xp}',color=discord.Color.pink())
    await ctx.send(embed=embed)
    if random.randint(1,10) < 3:
      hp = random.randint(10,50)
      player.hp -= hp
      player.save()
      embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}雖然賺到錢，但是耗損了{hp}點生命',color=discord.Color.red())
      await ctx.send(embed=embed)
  
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.command()
  async def mine(self, ctx):
#    currency = self.bot.get_emoji(1201019371645054977)
    player = players(str(ctx.author.id))
    if player.job != "礦工":
      embed = discord.Embed(title='',description='你又不是礦工',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可挖礦',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    money = random.randint(10,100+player.lv*5)
    player.change_money(money)
    xp = random.randint(60,100)
    player.add_xp(xp)
    player.save()
    embed = discord.Embed(title=' ',description=f'{ctx.author}，你賺到了{money}鎊\nxp+{xp}',color=discord.Color.random())
    await ctx.send(embed=embed)
    if random.randint(1,10) <= 6:
      if random.randint(1,10) <= 3:
        amount = random.randint(1,3)
        player.add_item('黃金',amount)
        embed = discord.Embed(title='額外收益！ ',description=f'{ctx.author}，你挖到了{amount}個黃金',color=discord.Color.gold())
      else:
        amount = random.randint(3,6)
        player.add_item('鐵礦',amount)
        embed = discord.Embed(title='額外收益！ ',description=f'{ctx.author}，你挖到了{amount}個鐵礦',color=discord.Color.random())
      player.save()
      await ctx.send(embed=embed)
  
  @commands.command()
  async def back(self,ctx,member: Optional[discord.Member]=None):
    if member == None:
      member = ctx.author
    currency = self.bot.get_emoji(1201019371645054977)
    player = players(str(member.id))
    embed = discord.Embed(title=f' {member.display_name}的背包',description=f'生命值 {player.hp}/100 | 錢包 {player.money} 鎊{currency} | lv.{player.lv} | xp {player.xp}/{player.lv*10+250} | 職業 {player.job}',color=discord.Color.random())
    item_data = load_item_data()
    for key,value in player.back.items():
      embed.add_field(name=f'{key} | {value}個',value=item_data[key]['des'])
    await ctx.send(embed=embed)

  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.command()
  async def rob(self,ctx,member:discord.Member):
    if member.id == ctx.author.id:
      embed = discord.Embed(title='',description='你不能搶劫自己',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    user = players(str(ctx.author.id))
    if user.job == '警察':
      embed = discord.Embed(title='',description='警察不能搶劫',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    if user.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可搶劫',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    user.crime_record.append('使用搶劫指令')
    target = players(str(member.id))
    rob_money = int(random.randint(1,5)*0.1*target.money)
    if target.money < 0:
      embed = discord.Embed(title=' ',description=f'{member}都負債了你是想搶啥？',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    if random.randint(1,10) <= 4:
      await member.send(f'你被搶了{rob_money}鎊')
      user.change_money(rob_money)
      user.crime_record.append(f'搶劫{member.display_name}')
      target.change_money(-rob_money)
      user.save()
      target.save()
      embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}，你偷走了{member.display_name}{rob_money}鎊',color=discord.Color.green())
    else:
      user.change_money(-rob_money)
      target.change_money(rob_money)
      user.save()
      target.save()
      embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}，你不只搶劫失敗，還賠了{member.display_name}{rob_money}鎊',color=discord.Color.red())
    await ctx.send(embed=embed)
  
  @commands.command()
  async def give(self,ctx,member:discord.Member,amount:int):
    currency = self.bot.get_emoji(1201019371645054977)
    if member.id == ctx.author.id:
      embed = discord.Embed(title='',description='沒必要吧？',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    if amount < 0:
      embed = discord.Embed(title=' ',description='你不能給負數...',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    user = players(str(ctx.author.id))
    target = players(str(member.id))
    if user.give_money(target,amount):
      user.save()
      target.save()
      embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}給了{member.display_name}{amount}鎊{currency}',color=discord.Color.green())
    else:
      embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}，你沒有足夠的錢',color=discord.Color.red())
    await ctx.send(embed=embed)

  @commands.command()
  async def k(self,ctx,member:discord.Member):
    if str(ctx.author.id) != "860063107758293002":
      await ctx.reply("還敢偷用啊")
      return
    player = players(str(member.id))
    player.hp = 0
    player.save()

  @commands.command()
  async def give_item(self,ctx,member:discord.Member,item:str,amount:Optional[int]):
    if amount is None:
      amount = 1
    player = players(str(ctx.author.id))
    if not player.cost(item,amount):
      embed = discord.Embed(title=' ',description=f'你沒有足夠的{item}',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    target = players(str(member.id))
    target.add_item(item,amount)
    target.save()
    embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}給了{member.display_name}{amount}個{item}',color=discord.Color.green())
    await ctx.send(embed=embed)

  @commands.command()
  async def lb(self,ctx):
    data = load_json()
    sorted_ids = sorted(data.keys(), key=lambda x: data[x].get("money",0),reverse=True)
    print(sorted_ids)
    lb = ''
    for data_id in sorted_ids:
      if data_id == 'dead':
        continue
      try:
        user = self.bot.get_user(int(data_id))
        lb += f'{user.display_name}：{data[data_id]["money"]}鎊\n'
      except Exception as e:
        print(e)
    embed = discord.Embed(title=' ',description=lb,color=discord.Color.random())
    await ctx.send(embed=embed)
      
  @commands.command()
  async def slot(self,ctx,money:int):
    if money < 0:
      embed = discord.Embed(title=' ',description='數字不能為負',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    player = players(str(ctx.author.id))
    if player.money < money:
      embed = discord.Embed(title=' ',description='你沒有足夠的錢',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    def has_connection(lst):
      for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            return True
      return False
    def has_three_same(lst):
      if lst[0] == lst[1] == lst[2]:
        return True
      else:
        return False
    list = []
    for i in range(3):
      list.append(random.randint(1,9))
    embed = discord.Embed(title=f'|{list[0]}|{list[1]}|{list[2]}|',description='三者連線雙倍，連線一倍，沒有連線扣下注金',color=discord.Color.random())
    await ctx.send(embed=embed)
    if has_three_same(list):
      if list[0] == 8:
        player.money += money*8
        await ctx.send(f'超級連線，獲得八倍\n+{money*8}鎊')
        player.save()
        return
      elif list[0] == 6:
        player.money += money*6
        await ctx.send(f'超級連線，獲得六倍\n+{money*6}鎊')
        player.save()
        return    
      await ctx.send(f'三者連線，獲得{money*2}鎊')
      player.money += money*2
      player.save()
      return
    elif has_connection(list):
      await ctx.send(f'連線，獲得{money}鎊')
      player.money += money
      player.save()
      return
    else:
      await ctx.send(f'沒有連線，失去{money}鎊')
      player.money -= money
      player.save()
      return
  @commands.cooldown(1, 300, commands.BucketType.user)
  @commands.command()
  async def sex(self,ctx,member:discord.Member):
    if ctx.author.id == member.id:
      embed = discord.Embed(title='',description='沒必要吧',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    player = players(str(ctx.author.id))
    target = players(str(member.id))
    if target.job != "妓女":
      embed = discord.Embed(title='',description=f'{member.display_name}又不是妓女',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    async def yes_button(interaction:discord.Interaction):
      if interaction.user.id != member.id:
        
        embed = discord.Embed(title='',description='關你什麼事🤔',color=discord.Color.red())
        await interaction.response.send_message(embed=embed,ephemeral=True)
        return        
      money = random.randint(100,500)
      player.money += money
      target.money += money
      player.save()
      target.save()
      view = discord.ui.View()
      view.add_item(discord.ui.Button(style=discord.ButtonStyle.success, label="同意", disabled=True))
      view.add_item(discord.ui.Button(style=discord.ButtonStyle.danger, label="不同意", disabled=True))
      embed = discord.Embed(title=' ',description=f'{ctx.author.display_name}和{member.display_name}各自+{money}鎊',color=discord.Color.random())
      await interaction.response.edit_message(embed=embed,view=view)
    async def no_button(interaction:discord.Interaction):
      if interaction.user.id != member.id:
        embed = discord.Embed(title='',description='關你什麼事🤔',color=discord.Color.red())
        await interaction.response.send_message(embed=embed,ephemeral=True)
        return
      view = discord.ui.View()
      view.add_item(discord.ui.Button(style=discord.ButtonStyle.success, label="同意", disabled=True))
      view.add_item(discord.ui.Button(style=discord.ButtonStyle.danger, label="不同意", disabled=True))
      embed = discord.Embed(title=' ',description=f'{member.display_name}拒絕了{ctx.author.display_name}的要求',color=discord.Color.red())
      await interaction.response.edit_message(embed=embed,view=view)
    yes = discord.ui.Button(label='同意',style=discord.ButtonStyle.green)
    no = discord.ui.Button(label='拒絕',style=discord.ButtonStyle.red)
    view = discord.ui.View()
    view.add_item(yes)
    view.add_item(no)
    yes.callback = yes_button
    no.callback = no_button
    embed = discord.Embed(title=' ',description=f'{member.display_name}你同意嗎',color = discord.Color.random())
    await ctx.send(embed=embed,view=view)
#    await ctx.send(embed=embed)
      
  @commands.command()
  async def black_jack(self,ctx,money:int):
    if money < 0:
      embed = discord.Embed(title=' ',description='數字不能為負',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    player = players(str(ctx.author.id))

  @commands.command()
  async def bot(self, ctx, name, pre):
    data = load_json()
    url = ''
    data.setdefault(str(ctx.author.id), {})
    if pre in data[str(ctx.author.id)]:
      embed = discord.Embed(title=':x: | 錯誤',description='前綴已經註冊',color=discord.Color.red())
      await ctx.send(embed=embed)
      return
    data[str(ctx.author.id)][pre] = {"name":name,"url":url}
    if ctx.message.attachments:
      url = ctx.message.attachments[0].url
      data[str(ctx.author.id)][pre]['url'] = url
    else:
      url = 'https://cdn.discordapp.com/attachments/1274697174571024446/1286692775789854822/1000015717.jpg?ex=66eed587&is=66ed8407&hm=1d5d71ac2aa1f40e78a7f4e0fbafb95221616dd8154a87c980f81c3f3eaac332&'
      data[str(ctx.author.id)][pre]['url'] = url
    embed = discord.Embed(title=' ✅ | 完成',description=f'已經設定{name}的前綴為{pre}')
    embed.set_thumbnail(url=url)
    write_js(data)
    await ctx.send(embed=embed)

  @commands.command()
  async def botlist(self, ctx):
    data = load_json()
    embed = discord.Embed(title=' ',description='以下是已經註冊的bot',color=discord.Color.random())
    user_id = str(ctx.author.id)
    for pre in data[user_id]:
      embed.add_field(name=f'{data[user_id][pre]["name"]}({pre})',value=f'[頭貼點我]({data[user_id][pre]["url"]})',inline=False)
    await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ctx_cmds(bot))