from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.app_commands import Choice
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data,load_item_data,generate_secret_number,evaluate_guess
from typing import Optional
from objects.player_object import players

class game_cmds(Cog_Extension):
  
  @app_commands.command(name = "開始遊戲", description = "使用指令開始遊戲:D")
  async def game_start(self, interaction: discord.Interaction):
    player = players(str(interaction.user.id))
    if interaction.channel.id != 1203004488340742214:
      embed = discord.Embed(title='',description='不能在這裡使用',color = discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
    try:
      id = interaction.user.id
      print(id)
      member_role = interaction.guild.get_role(1203004793833136229)
      member = interaction.guild.get_member(id)
      await member.add_roles(member_role)
      await interaction.response.send_message(f'嗨，{interaction.user.display_name}，歡迎:D\n需要幫忙就說喔~@我也可以哦;⁠)')
    except Exception as e:
      print(e)
#  @app_commands.cooldown(1, 10, commands.BucketType.user)

  @app_commands.command(name = "意見回饋", description = "使用指令反應對遊戲的意見")
  async def feedback(self, interaction: discord.Interaction):
    channel = self.bot.get_channel(1203005712205094922)
    class feedback_modal(discord.ui.Modal, title = "意見回饋"):
      feedback = discord.ui.TextInput(label = "意見", style = discord.TextStyle.long, placeholder = "請輸入意見", required = True, max_length = 500)
      async def on_submit(self, interaction: discord.Interaction):
        embed1 = discord.Embed(title = '', description = f"{self.feedback.value}", color = discord.Color.gold())
        embed1.set_author(name=f'{interaction.user.name}的建議',icon_url= interaction.user.avatar.url)
        embed2 = discord.Embed(title="傳送成功！", description="感謝您的意見", color=discord.Color.green())
        await channel.send(embed=embed1)
        await interaction.response.send_message(embed = embed2)
    await interaction.response.send_modal(feedback_modal())
  @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
  @app_commands.command(name = "工作",description="使用指令來工作")
  async def work(self, interaction: discord.Interaction):
    player = players(str(interaction.user.id))
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可工作',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    money = random.randint(10,100+player.lv*5)
    xp = random.randint(30,100)
    player.change_money(money)
    player.xp += xp
    player.save()
    embed = discord.Embed(title=' ',description=f'{interaction.user.display_name}賺到了{money}鎊\nxp+{xp}',color=discord.Color.random())
    await interaction.response.send_message(embed=embed)
    
  @app_commands.checks.cooldown(1, 10.0, key=lambda i: (i.guild_id, i.user.id))
  @app_commands.command(name="挖礦",description="使用指令以挖礦")
  async def app_mine(self, interaction:discord.Interaction):
#    currency = self.bot.get_emoji(1201019371645054977)
    player = players(str(interaction.user.id))
    if player.job != "礦工":
      embed = discord.Embed(title='',description='你又不是礦工',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可挖礦',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    money = random.randint(10,100+player.lv*5)
    player.change_money(money)
    xp = random.randint(60,100)
    player.add_xp(xp)
    player.save()
    embed = discord.Embed(title=' ',description=f'{interaction.user}，你賺到了{money}鎊\nxp+{xp}',color=discord.Color.random())
    await interaction.response.send_message(embed=embed)
    if random.randint(1,10) <= 6:
      if random.randint(1,10) <= 3:
        amount = random.randint(1,3)
        player.add_item('黃金',amount)
        embed = discord.Embed(title='額外收益！ ',description=f'{interaction.user}，你挖到了{amount}個黃金',color=discord.Color.gold())
      else:
        amount = random.randint(3,6)
        player.add_item('鐵礦',amount)
        embed = discord.Embed(title='額外收益！ ',description=f'{interaction.user}，你挖到了{amount}個鐵礦',color=discord.Color.random())
      player.save()
      await interaction.followup.send(embed=embed)

  @app_commands.command(name="背包",description="使用指令以查看背包")
  async def back(self,interaction:discord.Interaction,member: Optional[discord.Member]):
    if member is None:
      member = interaction.user
    currency = self.bot.get_emoji(1201019371645054977)
    player = players(str(member.id))
    embed = discord.Embed(title=f' {member.display_name}的背包',description=f'生命值 {player.hp}/100 | 錢包 {player.money} 鎊{currency} | lv.{player.lv} | xp {player.xp}/{player.lv*10+250} | 職業 {player.job}',color=discord.Color.random())
    item_data = load_item_data()
    for key,value in player.back.items():
      embed.add_field(name=f'{key} | {value}個',value=item_data[key]['des'])
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="搶劫",description="使用指令以搶劫別人的錢")
  async def rob(self,interaction:discord.Interaction,member:discord.Member):
    if member.id == interaction.user.id:
      embed = discord.Embed(title='',description='你不能搶劫自己',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    user = players(str(interaction.user.id))
    if user.job == '警察':
      embed = discord.Embed(title='',description='警察不能搶劫',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if user.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可搶劫',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    user.crime_record.append('使用搶劫指令')
    target = players(str(member.id))
    rob_money = int(random.randint(1,5)*0.1*target.money)
    if target.money < 0:
      embed = discord.Embed(title=' ',description=f'{member}都負債了你是想搶啥？',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if random.randint(1,10) <= 4:
      try:
        await member.send(f'你被搶了{rob_money}鎊')
      except Exception as e:
        print(e)
      user.change_money(rob_money)
      target.change_money(-rob_money)
      user.crime_record.append(f'搶劫{member.display_name}')
      user.save()
      target.save()
      embed = discord.Embed(title=' ',description=f'{interaction.user.display_name}，你偷走了{member.display_name}{rob_money}鎊',color=discord.Color.green())
    else:
      user.change_money(-rob_money)
      target.change_money(rob_money)
      user.save()
      target.save()
      embed = discord.Embed(title=' ',description=f'{interaction.user.display_name}，你不只搶劫失敗，還賠了{member.display_name}{rob_money}鎊',color=discord.Color.red())
    await interaction.response.send_message(embed=embed)
  
  @app_commands.command(name="給予金錢",description="使用指令以給予別人錢")
  async def give(self,interaction:discord.Interaction,member:discord.Member,amount:int):
    
    currency = self.bot.get_emoji(1201019371645054977)
    if member.id == interaction.user.id:
      embed = discord.Embed(title='',description='沒必要吧？',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if amount < 0:
      embed = discord.Embed(title=' ',description='你不能給負數...',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    user = players(str(interaction.user.id))
    target = players(str(member.id))
    if user.give_money(target,amount):
      user.save()
      target.save()
      embed = discord.Embed(title=' ',description=f'{interaction.user.display_name}給了{member.display_name}{amount}鎊{currency}',color=discord.Color.green())
    else:
      embed = discord.Embed(title=' ',description=f'{interaction.user.display_name}，你沒有足夠的錢',color=discord.Color.red())
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="給予物件",description="使用指令以給予別人物件")
  async def give_item(self,interaction:discord.Interaction,member:discord.Member,item:str,amount:Optional[int]):
    if amount is None:
      amount = 1
    if amount < 0:
      embed = discord.Embed(title=' ',description='你不能給負數...',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player = players(str(interaction.user.id))
    if not player.cost(item,amount):
      embed = discord.Embed(title=' ',description=f'你沒有足夠的{item}',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    target = players(str(member.id))
    target.add_item(item,amount)
    embed = discord.Embed(title=' ',description=f'{interaction.user.display_name}給了{member.display_name}{amount}個{item}',color=discord.Color.green())
    target.save()
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="職業",description="使用指令以選擇或轉換職業")
  @app_commands.choices(
    job = [
    Choice(name="妓女",value="妓女"),
    Choice(name="警察",value="警察"),
    Choice(name="礦工",value="礦工"),
    Choice(name="駭客",value="駭客")
    ]
  )
  async def job(self,interaction:discord.Interaction,job:Choice[str]):
    player = players(str(interaction.user.id))
    if player.lv < 5:
      embed = discord.Embed(title=' ',description='必須有五等才能選擇或轉換職業！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player.lv -= 5
    player.job = job.value
    player.save()
    member_role = interaction.guild.get_role(1203675286227656705)
    member = interaction.guild.get_member(interaction.user.id)
    if member_role in member.roles:
      await member.remove_roles(member_role)
    if job.value == "警察":
      await member.add_roles(member_role)
    embed = discord.Embed(title=' ',description=f'{interaction.user.display_name}的職業已經更改為{job.name}\n消耗五等',color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="查看犯罪紀錄",description="警察專屬，使用指令追查罪犯")
  async def check_crime_record(self,interaction:discord.Interaction,member:discord.Member):
    player = players(str(interaction.user.id))
    if player.job != "警察":
      embed = discord.Embed(title=' ',description='你又不是警察',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    target = players(str(member.id))
    des = ''
    for crime in target.crime_record:
      des += f'{crime} '
    if des == '':
      des += '空空如也:('
    des += f'\n共計{len(target.crime_record)}次犯罪'
    embed = discord.Embed(title=f'{member.display_name}的犯罪紀錄',description=des)
    await interaction.response.send_message(embed=embed)

  @app_commands.checks.cooldown(1, 300.0, key=lambda i: (i.guild_id, i.user.id))
  @app_commands.command(name="逮捕",description="警察專屬，使用指令逮捕別人")
  async def arrest(self,interaction:discord.Interaction,member:discord.Member):
    if member.id == interaction.user.id:
      embed = discord.Embed(title='',description='你不能逮捕自己',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player = players(str(interaction.user.id))
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可逮捕其他人',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if player.job != "警察":
      embed = discord.Embed(title='',description='你又不是警察',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    target = players(str(member.id))
    if len(target.crime_record) == 0:
      embed = discord.Embed(title='',description='他沒有犯過任何罪',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    money = len(target.crime_record)*750
    xp = len(target.crime_record)*100
    target.crime_record = []
    target.money -= money
    player.money += money
    player.xp += xp
    target.save()
    player.save()
    embed = discord.Embed(title='',description=f'你逮捕了{member.display_name}！\n錢包+{money}鎊\nxp+{xp}',color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
    await member.send(f'你被警察逮捕了，扣{money}鎊')

  @app_commands.command(name="清洗犯罪紀錄",description="駭客專屬，清洗別人的犯罪紀錄")
  async def clean_crime_record(self,interaction:discord.Interaction,member:discord.Member):
    if member.id == interaction.user.id:
      embed = discord.Embed(title='',description='你不能清洗自己的犯罪紀錄',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player = players(str(interaction.user.id))
    if player.job != "駭客":
      embed = discord.Embed(title='',description='你又不是駭客',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可清洗其他人的犯罪紀錄',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if player.lv < 3:
      embed = discord.Embed(title='',description='必須有三等才能清洗犯罪紀錄',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    target = players(str(member.id))
    target.crime_record = []
    target.save()
    player.lv -= 3
    player.crime_record.append('駭入系統清洗犯罪紀錄')
    player.save()
    embed = discord.Embed(title='',description=f'你駭入系統清洗了{member.display_name}的犯罪紀錄\n耗損3等\n現在你被計上一筆記錄了！',color=discord.Color.green())
    await interaction.response.send_message(embed=embed,ephemeral=True)
    channel = self.bot.get_channel(1203720543149228094)
    embed = discord.Embed(title='警報！',description='有人駭入了系統！一份犯罪紀錄遭到清除！',color=discord.Color.red())
    await channel.send(embed=embed)

  @app_commands.command(name="1a2b",description="使用指令來玩1a2b")
  async def app_1a2b(self,interaction:discord.Interaction):
    times = 0
    secret = generate_secret_number()
    embed = discord.Embed(title='1a2b遊戲',description=f'你猜了{times}次',color=discord.Color.gold())
    view = discord.ui.View()
    guess_button =discord.ui.Button(label='猜測數字',style=discord.ButtonStyle.green)
    async def guess_button_callback(interaction:discord.Interaction):
      if interaction.user.id != interaction.message.interaction.user.id:
        embed = discord.Embed(title=' ',description='關你什麼事啊🤔',color=discord.Color.red())
        await interaction.response.send_message(embed=embed,ephemeral=True)
      class Modal(discord.ui.Modal,title = "1a2b好玩遊戲:D"):
        ans = discord.ui.TextInput(label="猜測一個四位數字！",placeholder="輸入數字",style=discord.TextStyle.short,max_length=4)
        async def on_submit(self,interaction:discord.Interaction):
          guess = self.ans.value
          nonlocal times 
          times += 1
          try:
            int(guess)
            result = evaluate_guess(guess,secret)
            if result == '4A0B':
              embed = discord.Embed(title='1a2b遊戲',description=f'在猜了{times}次以後，你猜中答案「{secret}」，你贏了！',color = discord.Color.green())
              await interaction.response.edit_message(embed=embed,view=None)
            else:
              embed = discord.Embed(title='1a2b遊戲',description=f'你猜了{times}次\n{guess}的結果是：{result}',color=discord.Color.gold())
              await interaction.response.edit_message(embed=embed)
          except:
            embed = discord.Embed(title='1a2b遊戲',description='請輸入四位整數！',color=discord.Color.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
      await interaction.response.send_modal(Modal())
    guess_button.callback = guess_button_callback
    view.add_item(guess_button)
    await interaction.response.send_message(embed=embed,view=view)
     

async def setup(bot):
    await bot.add_cog(game_cmds(bot))