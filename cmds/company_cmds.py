from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data,load_bank_data,write_bank_data,load_company_data,write_company_data
from objects.player_object import players
from typing import Optional

class company_cmds(Cog_Extension):

  @app_commands.command(name="創建公司",description="使用指令以創建公司")
  async def build_company(self,interaction:discord.Interaction,name:str,description:str):
    player = players(str(interaction.user.id))

async def setup(bot):
    await bot.add_cog(company_cmds(bot))