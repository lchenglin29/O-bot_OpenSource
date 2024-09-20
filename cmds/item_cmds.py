from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from discord.app_commands import Choice
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data,load_item_data,write_item_data
from typing import Optional
from objects.player_object import players


class item_cmds(Cog_Extension):
  
  @app_commands.command(name = "建立物件", description = "使用指令自定義物件")
  @app_commands.describe(
    name = "物件名稱",
    des = "物件敘述",
    make_by = "合成原料",
    private = "是否僅建立者可合成",
    atk = "使用物件的攻擊力",
    hp = "使用物件回復的生命值"
  )
  @app_commands.choices(
    make_by = [
      Choice(name = "鐵礦",value = "鐵礦"),
      Choice(name = "黃金",value = "黃金"),
      Choice(name = "O-鎊",value = "鎊")
    ]
  )
  async def build_item(self, interaction: discord.Interaction,name:str,des:str,make_by:Choice[str], private:bool,atk:Optional[int],hp: Optional[int]):
    item_data = load_item_data()
    if name in item_data:
      embed = discord.Embed(title='',description='物件已存在',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if atk is None and hp is None:
      embed = discord.Embed(title='', description='數值都沒有，你要這東西幹嘛？',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    item_data.setdefault(name,{"des":des,"maker":str(interaction.user.id)})
    cost = 0
    if atk is not None:
      if atk < 0:
        embed = discord.Embed(title='', description='攻擊力不能小於0',color=discord.Color.red())
        await interaction.response.send_message(embed=embed,ephemeral=True)
        return
      item_data[name].setdefault("atk",atk)
      cost += atk
    if hp is not None:
      if hp < 0:
        embed = discord.Embed(title='', description='血量不能小於0',color=discord.Color.red())
        await interaction.response.send_message(embed=embed,ephemeral=True)
        return
      item_data[name].setdefault("hp",hp)
      cost += hp
    if make_by.value == "鐵礦":
      item_data[name].setdefault("make_by","鐵礦")
      cost *= 5
    elif make_by.value == "黃金":
      item_data[name].setdefault("make_by","黃金")
      cost *= 3
    else:
      item_data[name].setdefault("make_by","鎊")
      cost *= 50
    if private:
      item_data[name].setdefault("private",True)
    else:
      item_data[name].setdefault("private",False)
    item_data[name].setdefault("cost",cost)
    embed = discord.Embed(title='物件已建立', description=f'合成物件__**{name}**__所需成本**{cost}**{make_by.value}',color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
    write_item_data(item_data)

  @app_commands.command(
    name="刪除物件",
    description="使用指令刪除物件"
  )
  async def delete_item(self, interaction: discord.Interaction,name:str):
    item_data = load_item_data()
    if name not in item_data:
      embed = discord.Embed(title='',description='物件不存在',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if "maker" not in item_data[name]:
      embed = discord.Embed(title='',description='你沒有權限刪除此物件',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if item_data[name]["maker"] != str(interaction.user.id):
      embed = discord.Embed(title='',description='你沒有權限刪除此物件',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    data = load_json()
    using = False
    for key,value in data.items():
      if key == "dead":
        continue
      if name in data[key]["back"]:
        using = True
        break
      else:
        pass
    if using:
      embed = discord.Embed(title='',description='物件還有人使用中，無法刪除',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    item_data.pop(name)
    embed = discord.Embed(title='物件已刪除',description=f'物件__**{name}**__已被刪除',color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
    write_item_data(item_data)

  @app_commands.command(
    name="物件列表",
    description="使用指令查看物件列表"
  )
  async def item_list(self, interaction: discord.Interaction):
    item_data = load_item_data()
    embed = discord.Embed(title='物件列表',color=discord.Color.gold())
    for key,value in item_data.items():
      try:
        if value["maker"] == str(interaction.user.id):
          embed.add_field(name=f'{key} | 成本{value["cost"]}{value["make_by"]} | 私人製作 {value["private"]}',value=value["des"])
      except Exception as e:
        print(e)
        continue
    if embed.fields == []:
      embed = discord.Embed(title='物件列表',description='空空如也:(',color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

  @app_commands.command(
    name="合成物件",
    description="使用指令合成物件"
  )
  async def make_item(self, interaction: discord.Interaction,name:str,amount:Optional[int]):
    if amount is None:
      amount = 1
    if amount < 0:
      embed = discord.Embed(title='',description='你不能合成負數個物件...',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    item_data = load_item_data()
    if name not in item_data:
      embed = discord.Embed(title='',description='物件不存在',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if "make_by" not in item_data[name]:
      embed = discord.Embed(title='',description='此物件不可合成',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
    if item_data[name]["private"]:
      if str(interaction.user.id) != item_data[name]["maker"]:
        embed = discord.Embed(title='',description='此物件僅可由製作者合成',color=discord.Color.red())
        return
    player = players(str(interaction.user.id))
    if player.cost(item_data[name]["make_by"],item_data[name]["cost"]*amount):
      embed = discord.Embed(title=f'已合成{name}{amount}個',description=f'耗費{item_data[name]["cost"]*amount}{item_data[name]["make_by"]}',color=discord.Color.green())
      player.add_item(name,amount)
      player.save()
      await interaction.response.send_message(embed=embed)
      return
    else:
      embed = discord.Embed(title='',description=f'你的{item_data[name]["make_by"]}不夠',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)

  @app_commands.command(
    name="使用武器",
    description="使用指令以使用武器"
  )
  async def use_weapon(self, interaction: discord.Interaction,name:str,amount:Optional[int],member:discord.Member):
    if amount is None:
      amount = 1
    if amount < 0:
      embed = discord.Embed(title='',description='數字不能為負',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    item_data = load_item_data()
    player = players(str(interaction.user.id))
    if player.hp <= 0:
      embed = discord.Embed(title='',description='生命值為0時不可攻擊',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if name not in player.back:
      embed = discord.Embed(title='',description='你沒有這個東西！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if "atk" not in item_data[name]:
      embed = discord.Embed(title='',description='這又不是武器',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    target = players(str(member.id))
    if not player.cost(name,amount):
      embed = discord.Embed(title='',description=f'你的{name}不夠',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return  
    if target.hp <= 0:
      embed = discord.Embed(title='',description=f'{member.display_name}已經不能再受到攻擊了',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    d = False
    try:
#      player.save()
      if target.hp - item_data[name]["atk"]*amount <= 0:
        target.hp = 0
        d = True
        target.save()
      else:
        target.hp -= item_data[name]["atk"]*amount
        target.save()
      atk = item_data[name]["atk"]*amount
      embed = discord.Embed(title="噢噢",description=f"{interaction.user.display_name}使用{amount}個{name}對{member.display_name}造成了{atk}點傷害！",color=discord.Color.random())
      await interaction.response.send_message(embed=embed)
      if d:
        embed = discord.Embed(title=' 喔不！',description=f'{member.display_name}被{interaction.user.display_name}的{name}打倒了！',color=discord.Color.red())
        if player.job == "警察":
          embed2 = discord.Embed(title="糟糕！",description=f"{interaction.user.display_name}，你身為警察不該這樣的！\n你被開除了！",color=discord.Color.red())
          await interaction.channel.send(embed=embed2)
          palyer.job == "普通人"
          user = self.bot.get_user(player.id)
          police_role = self.bot.get_role(1203675286227656705)
          user.remove_roles(police_role)
        player.crime_record.append(f'{interaction.user.display_name}使用{name}打倒{member.display_name}')
        player.save()
        await interaction.followup.send(embed=embed)
    except Exception as e:
      print(e)

  @app_commands.command(name="使用回復道具",description="使用指令以使用回復道具")
  async def use_recovery(self, interaction: discord.Interaction,name:str,amount:Optional[int]):
    if amount is None:
      amount = 1
    if amount < 0:
      embed = discord.Embed(title='',description='數字不能為負',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    item_data = load_item_data()
    if name not in item_data:
      embed = discord.Embed(title='',description='物件不存在',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if "hp" not in item_data[name]:
      embed = discord.Embed(title='',description='這又不是回復道具',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    player = players(str(interaction.user.id))
    if not player.cost(name,amount):
      embed = discord.Embed(title='',description=f'你的{name}不夠',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if item_data[name]["hp"]*amount + player.hp > 100:
      player.hp = 100
    else:
      player.hp += item_data[name]["hp"]*amount
    data = load_json()
    try:
      if str(interaction.user.id) in data["dead"]:
        data["dead"].pop(str(interaction.user.id))
        write_js(data)
    except Exception as e:
      print(e)
    player.save()
    embed = discord.Embed(title="生命回復！",description=f"{interaction.user.display_name}使用了{amount}個{name}，回復了{item_data[name]['hp']*amount}點生命值！",color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name="物件資訊",description="使用指令以查看物件資訊")
  async def item_info(self, interaction: discord.Interaction,name:str):
    item_data = load_item_data()
    if name not in item_data:
      embed = discord.Embed(title='',description='物件不存在',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    embed = discord.Embed(title=f'物件__**{name}**__',color=discord.Color.gold())
    embed.add_field(name='描述',value=item_data[name]["des"])
    if "maker" in item_data[name]:
      embed.add_field(name='建造者',value=f'<@{item_data[name]["maker"]}>')
    if "cost" in item_data[name]:
      embed.add_field(name='成本',value=f'{item_data[name]["cost"]}{item_data[name]["make_by"]}')
    if "private" in item_data[name]:
      embed.add_field(name='私人製作',value=item_data[name]["private"])
    effect = ""
    if "hp" in item_data[name]:
      effect += f'回復{item_data[name]["hp"]}點生命值\n'
    if "atk" in item_data[name]:
      effect += f'造成{item_data[name]["atk"]}點傷害'
    embed.add_field(name='效果',value=effect)
    await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(item_cmds(bot))