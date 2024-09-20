from discord import member
import discord
from discord.ext import tasks, commands
from core.core import Cog_Extension
from mydef.mydef import load_json,write_js,now_data,load_bank_data,write_bank_data
from objects.player_object import players

class task(Cog_Extension):
  def __init__(self, bot):
      super().__init__(bot)
      self.check_level.start()
      self.check_hp.start()
  def cog_unload(self):
    print('TASK已停止')  
    self.check_level.cancel()
    self.check_hp.cancel()
  
  @tasks.loop(seconds = 3)
  async def check_level(self):
    data = load_json()
    for user_id in data:
      if user_id == 'dead':
        continue 
      if data[user_id]["xp"] >=data[user_id]["lv"]*10+250:
        data[user_id]["xp"] -= data[user_id]["lv"]*10+250
        data[user_id]["lv"] += 1
        write_js(data)
      else:
        pass
    print('\033[32m等級及經驗值檢核完成\033[0m')

  @tasks.loop(seconds = 3)
  async def check_hp(self):
    data = load_json()
    list = []
    for user_id in data:
#      if user_id in data["dead"]:
#        continue
      if user_id == 'dead':
        continue
      if data[user_id]["hp"] == 0:
        if user_id in data["dead"]:
          continue
        try:
          player = players(user_id)
          user = self.bot.get_user(int(user_id))
          if player.money < 0:
            cm = int(player.money*0.6-100)
            player.change_money(cm)
            player.save()
            embed = discord.Embed(title='死亡！', description=f'錢包{cm}鎊\n等級-{int(player.lv*0.3)}',color=discord.Color.red())
            await user.send(embed=embed)
          elif player.money > 0:
            cm = -(int(player.money*0.6)+100)
            player.change_money(cm)
            player.save()
            embed = discord.Embed(title='死亡！', description=f'錢包{cm}鎊\n等級-{int(player.lv*0.3)}',color=discord.Color.red())
            await user.send(embed=embed)
          elif player.money == 0:
            player.change_money(-1000)
            player.save()
            embed = discord.Embed(title='死亡！', description='錢包-1000鎊\n等級-{int(player.lv*0.3)}',color=discord.Color.red())
            await user.send(embed=embed)
          player.lv -= int(player.lv*0.3)
          player.save()
          data["dead"].setdefault(user_id,True)
        except Exception as e:
          print(f'\033[31mAn error occurred: {e}\033[0m')
      else:
        pass
    now_data = load_json()
    now_data["dead"] = data["dead"]
    write_js(now_data)
    print(f'\033[32m生命值檢核完成\n共計：{len(list)}人死亡\033[0m')

  @tasks.loop(seconds = 1800)
  async def 利息(self):
    bank_data = load_bank_data()
    for key,value in bank_data.items():
      bank_data[key]["balance"] += int(bank_data[key]["balance"]*0.01)
    write_bank_data(bank_data)
    print('\033[32m利息檢核完成\033[0m')
    channel = self.bot.get_channel(1204360688340963330)
    await channel.send('利息檢核完成')

async def setup(bot: commands.Bot):
    await bot.add_cog(task(bot))