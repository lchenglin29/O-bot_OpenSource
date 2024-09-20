from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data
from typing import Optional
from objects.player_object import players

class pass_cmds(Cog_Extension):
  
  @app_commands.command(name = "自動通關", description = "使用指令以通關")
  @app_commands.describe(nationality= "輸入持有的國籍",place_of_entry="輸入連結的來源",purpose="輸入入籍的目的")
  async def pass_cmd(self, interaction: discord.Interaction, nationality:str,place_of_entry:str,purpose:str):
    if interaction.channel.id != 1156196541388832778:
      await interaction.response.send_message(content='請在<#1156196541388832778>使用此指令' ,ephemeral=True)
      return
    embed = discord.Embed(title=' 自動通關',description=f'時間 {now_data()}' ,color=discord.Color.green())
    embed.add_field(name='入境時姓名',value=interaction.user.display_name)
    embed.add_field(name='Discord使用者ID',value=interaction.user.id)
    embed.add_field(name='使用國籍',value=nationality,inline=True)
    embed.add_field(name='來源',value=place_of_entry,inline=True)
    embed.add_field(name='目的',value=purpose,inline=True)
    embed.set_thumbnail(url=interaction.user.display_avatar)
    try:
      member = interaction.guild.get_member(interaction.user.id)
      role = interaction.guild.get_role(1161651783651819691)
      await member.add_roles(role)
    except Exception as e:
      print(e)
    channel = self.bot.get_channel(1201775466680430653)
    await channel.send(embed=embed)
    await interaction.response.send_message(f'嗨，**{interaction.user.display_name}**，歡迎來到**威爾蘭**！')
async def setup(bot):
    await bot.add_cog(pass_cmds(bot))