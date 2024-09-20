from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data,load_bank_data,write_bank_data
from typing import Optional

class bank_cmd(Cog_Extension):
  
  @app_commands.command(name='銀行-註冊',description='註冊一個銀行帳戶 *請不要使用你任何真實帳戶的密碼！')
  @app_commands.describe(name = "使用者名稱", password = "密碼 *再度提醒，請不要使用你任何真實帳戶的密碼！")
  async def register(self,interaction:discord.Interaction,name:str,password:str):
    data = load_json()
    bank_data = load_bank_data()
    if "log_in" in data[str(interaction.user.id)]:
      embed = discord.Embed(title='欸不是，你還在登入狀態耶！',description='先登出再使用好不好owo',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if name not in bank_data:
      bank_data.setdefault(name,{"password":password,"balance":0})
      data[str(interaction.user.id)].setdefault("log_in",name)
      write_js(data)
      write_bank_data(bank_data)
      embed = discord.Embed(title='帳戶已創建！',description=f'使用</銀行-查看帳號:1143492793545789560>以查詢餘額 | 帳號：{name} | 密碼{password}',color=discord.Color.green())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if name in bank_data:
      embed = discord.Embed(title='該帳戶名稱已被使用了！',description='試試看別的名稱？')
      await interaction.response.send_message(embed=embed,ephemeral=True)
    return

  @app_commands.command(name='銀行-登入',description='登入帳戶')
  async def log_in(self,interaction:discord.Interaction,name:str,password:str):
    data = load_json()
    bank_data = load_bank_data()
    member_id = str(interaction.user.id)
    if "log_in" in data[member_id]:
      embed = discord.Embed(title='你在登入狀態！',description=f'你登入的身分是：{data[member_id]["log_in"]}',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if name not in bank_data:
      embed = discord.Embed(title=':x: | 錯誤！',description='帳戶或密碼有誤',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if password != bank_data[name]["password"]:
      embed = discord.Embed(title=':x: | 錯誤！',description='帳戶或密碼有誤',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if bank_data[name]["password"] == password:
      data[member_id].setdefault("log_in",name)
      write_js(data)
      write_bank_data(bank_data)
      embed = discord.Embed(title='已登入！',description=f'你目前登入的身分是：{name}',color=discord.Color.green())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return

  @app_commands.command(name='銀行-登出',description='登出銀行帳戶')
  async def log_out(self,interaction:discord.Interaction):
    data = load_json()
    bank_data = load_bank_data()
    if "log_in" not in data[str(interaction.user.id)]:
     embed = discord.Embed(title='請先登入！',color=discord.Color.red())
     await interaction.response.send_message(embed=embed,ephemeral=True)
     return
    data[str(interaction.user.id)].pop("log_in")
    write_js(data)
    write_bank_data(bank_data)
    embed = discord.Embed(title='已登出！',color=discord.Color.green())
    await interaction.response.send_message(embed=embed,ephemeral=True)

  @app_commands.command(name='銀行-查看帳號',description='查看銀行帳戶的資訊')
  async def balance(self,interaction:discord.Interaction):
    data = load_json()
    bank_data = load_bank_data()
    if "log_in" not in data[str(interaction.user.id)]:
      embed = discord.Embed(title='請先登入！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    embed = discord.Embed(title='銀行帳戶',description=f'目前登入身分：{data[str(interaction.user.id)]["log_in"]}',color=discord.Color.green())
    embed.add_field(name='帳戶詳細資訊',value=f'帳戶名稱：{data[str(interaction.user.id)]["log_in"]} | 密碼：{bank_data[data[str(interaction.user.id)]["log_in"]]["password"]}')
    embed.add_field(name='現金',value=data[str(interaction.user.id)]["money"],inline=False)
    embed.add_field(name='帳戶餘額',value=bank_data[data[str(interaction.user.id)]["log_in"]]["balance"],inline=False)
    await interaction.response.send_message(embed=embed,ephemeral=True)

  @app_commands.command(name='銀行-存入')
  async def dep(self,interaction:discord.Interaction,amount:int):
    if amount < 0:
      embed = discord.Embed(title='',description='你不能存入負數...',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    data = load_json()
    bank_data = load_bank_data()
    if "log_in" not in data[str(interaction.user.id)]:
      embed = discord.Embed(title='請先登入！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if amount > data[str(interaction.user.id)]["money"]:
      embed = discord.Embed(title='你的現金不夠！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    data[str(interaction.user.id)]["money"] -= amount
    bank_data[data[str(interaction.user.id)]["log_in"]]["balance"] += amount
    write_js(data)
    write_bank_data(bank_data)
    embed = discord.Embed(title=f'已將{amount}存入{data[str(interaction.user.id)]["log_in"]}！',description=f'使用</銀行-查看帳號:1143492793545789560>以查詢餘額',color=discord.Color.green())
    await interaction.response.send_message(embed=embed,ephemeral=True)

  @app_commands.command(name='銀行-提領')
  async def with_money(self,interaction:discord.Interaction,amount:int):
    if amount < 0:
      embed = discord.Embed(title='',description='你不能提領負數...',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    data = load_json()
    bank_data = load_bank_data()
    if "log_in" not in data[str(interaction.user.id)]:
      embed = discord.Embed(title='請先登入！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if amount > bank_data[data[str(interaction.user.id)]["log_in"]]["balance"]:
      embed = discord.Embed(title='你的餘額不夠！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    data[str(interaction.user.id)]["money"] += amount
    bank_data[data[str(interaction.user.id)]["log_in"]]["balance"] -= amount
    write_js(data)
    write_bank_data(bank_data)
    embed = discord.Embed(title=f'已從{data[str(interaction.user.id)]["log_in"]}提領{amount}！',description=f'使用</銀行-查看帳號:1143492793545789560>以查詢餘額',color=discord.Color.green())
    await interaction.response.send_message(embed=embed,ephemeral=True)
  
  @app_commands.command(name='銀行-匯款')
  @app_commands.describe(name='欲匯款的帳號！')
  async def transfer(self,interaction:discord.Interaction,name:str,amount:int):
    if amount < 0:
      embed = discord.Embed(title='',description='你不能匯款負數...',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    data = load_json()
    bank_data = load_bank_data()
    if "log_in" not in data[str(interaction.user.id)]:
      embed = discord.Embed(title='請先登入！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if amount > bank_data[data[str(interaction.user.id)]["log_in"]]["balance"]:
      embed = discord.Embed(title='你的餘額不夠！',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    if name not in bank_data:
      embed = discord.Embed(title='找不到的用戶',description='',color=discord.Color.red())
      await interaction.response.send_message(embed=embed,ephemeral=True)
      return
    bank_data[data[str(interaction.user.id)]["log_in"]]["balance"] -= amount
    bank_data[name]["balance"] += amount
    write_bank_data(bank_data)
    embed = discord.Embed(title=f'已匯款{amount}到{name}！',color=discord.Color.green())
    await interaction.response.send_message(embed=embed)
      
async def setup(bot):
    await bot.add_cog(bank_cmd(bot))