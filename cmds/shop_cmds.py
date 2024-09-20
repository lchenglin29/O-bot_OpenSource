from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data
from objects.player_object import players
from typing import Optional

class shop_cmds(Cog_Extension):
  
  @app_commands.command(name = "上架商店", description = "使用指令以將物件上架至個人商店")
  async def shop_update(self, interaction: discord.Interaction,item:str,price:int,amount:Optional[int]):
    if amount is None:
      amount = 1
    if price < 0:
      embed = discord.Embed(title=' ',description='價格不能為負',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if amount < 0:
      embed = discord.Embed(title='',description='數量不能為負',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player = players(str(interaction.user.id))
    if item not in player.back:
      embed = discord.Embed(title=' ',description=f'你沒有{item}',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if player.back[item] < amount:
      embed = discord.Embed(title='',description=f'你的{item}不夠',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player.back[item] -= amount
    player.shop.setdefault(item,{"amount":0,"price":price})
    player.shop[item]["amount"] += amount
    player.save()
    embed = discord.Embed(title=' ',description=f'已上架{amount}個{item}至商店',color=discord.Color.green())
    embed.add_field(name='單價',value=price)
    await interaction.response.send_message(embed=embed) 

  @app_commands.command(name = "下架商店", description = "使用指令以將物件下架")
  async def shop_delete(self, interaction: discord.Interaction,item:str,amount:Optional[int]):
    if amount is None:
      amount = 1
    if amount < 0:
      embed = discord.Embed(title=' ',description='數量不能為負',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player = players(str(interaction.user.id))
    if item not in player.shop:
      embed = discord.Embed(title=' ',description=f'你的商店沒有{item}',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if player.shop[item]["amount"] < amount:
      embed = discord.Embed(title='',description=f'你商店中的{item}不夠',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player.shop[item]["amount"] -= amount
    player.back.setdefault(item,0)
    player.back[item] += amount
    if player.shop[item]["amount"] == 0:
      player.shop.pop(item)
    player.save()
    embed = discord.Embed(title=' ',description=f'已下架{amount}個{item}至背包',color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name = "商店", description = "使用指令以查看個人商店")
  async def shop(self,interaction:discord.Interaction,member:Optional[discord.Member]):
    if member is None:
      member = interaction.user
    player = players(str(member.id))
    description = ''
    if len(player.shop) == 0:
      description = '空空如也:('
    embed = discord.Embed(title=f'{member.display_name}的商店',description=description,color=discord.Color.random())
    for key,value in player.shop.items():
      embed.add_field(name=f'{key} | {value["amount"]}個',value=f'單價{value["price"]}')
    await interaction.response.send_message(embed=embed)

  @app_commands.command(name = "購買", description = "使用指令以購買物品")
  async def buy(self,interaction:discord.Interaction,member:discord.Member,item:str,amount:Optional[int]):
    if member.id == interaction.user.id:
      embed = discord.Embed(title=' ',description='沒必要吧？',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if amount is None:
      amount = 1
    if amount < 0:
      embed = discord.Embed(title=' ',description='數量不能為負',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    player = players(str(interaction.user.id))
    target = players(str(member.id))
    if item not in target.shop:
      embed = discord.Embed(title=' ',description=f'{member.display_name}沒有賣{item}',color = discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if amount > target.shop[item]["amount"]:
      embed = discord.Embed(title=' ',description=f'{member.display_name}的{item}不夠',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    if amount*target.shop[item]["price"] > player.money:
      embed = discord.Embed(title=' ',description=f'你沒有足夠的錢',color=discord.Color.red())
      await interaction.response.send_message(embed=embed)
      return
    cost = amount*target.shop[item]["price"]
    player.money -= amount*target.shop[item]["price"]
    target.money += amount*target.shop[item]["price"]
    player.back.setdefault(item,0)
    player.back[item] += amount
    target.shop[item]["amount"] -= amount
    if target.shop[item]["amount"] == 0:
      target.shop.pop(item)
    player.save()
    target.save()
    embed = discord.Embed(title='交易明細',description=f'{interaction.user.display_name}向{member.display_name}購買了{amount}個{item}\n共計{cost}鎊',color=discord.Color.green())
    await member.send(embed=embed)
    await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(shop_cmds(bot))