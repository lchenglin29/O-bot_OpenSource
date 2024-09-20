from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data
from typing import Optional

class template(Cog_Extension):
  
  @app_commands.command(name = "範本指令", description = "提供之後寫互動式指令的一個範本")
  async def template(self, interaction: discord.Interaction):
      await interaction.response.send_message("""__這是用了Cog架構的程式，不需使用的模組**可以自行刪除**__
*mydef是我自己寫的一些函式*
```py
from os import name
import discord,asyncio,aiohttp,datetime,random
from discord import InteractionMessage, app_commands
from discord.ext import commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data
from typing import Optional

class template(Cog_Extension):
  
  @app_commands.command(name = "範本指令", description = "提供之後寫互動式指令的一個範本")
  async def template(self, interaction: discord.Interaction):
      await interaction.response.send_message('嗨')
async def setup(bot):
    await bot.add_cog(template(bot))
      ```""")
async def setup(bot):
    await bot.add_cog(template(bot))