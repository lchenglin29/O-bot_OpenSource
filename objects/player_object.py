from mydef.mydef import load_json,write_js

class players():
  def __init__(self, id:str):
    self.id = id
    data = load_json()
    if self.id not in data:
      data.setdefault(id,{"money":0,"back":{},"lv":0,"hp":100,"xp":0,"crime_record":[],"job":"普通人","shop":{}})
      write_js(data)
    data = load_json()
    user_data = data[self.id]
    remove_list = []
    for key,value in user_data["back"].items():
      if value <= 0:
        remove_list.append(key)
    if len(remove_list) > 0:
      for key in remove_list:
        user_data["back"].pop(key)
      data[self.id] = user_data
      write_js(data)
      data = load_json()
      user_data = data[self.id]
    self.money = user_data["money"]
    self.back = user_data["back"]
    self.lv = user_data["lv"]
    self.hp = user_data["hp"]
    self.xp = user_data["xp"]
    self.job = user_data["job"]
    self.shop = user_data["shop"]
    self.crime_record = user_data["crime_record"]
  def change_money(self, money:int):
    self.money += money
  def add_xp(self, xp:int):
    self.xp += xp
  def save(self):
    data = load_json()
    user_data = {"money":self.money,"back":self.back,"lv":self.lv,"hp":self.hp,"xp":self.xp,"job":self.job,"crime_record":self.crime_record,"shop":self.shop}
    if "log_in" in data[self.id]:
      user_data.setdefault("log_in",data[self.id]["log_in"])
    data[self.id] = user_data
    write_js(data)
  def give_money(self, to, amount:int):
    if self.money < amount:
      return False
    self.change_money(-amount)
    to.change_money(amount)
    return True
  def add_item(self, item:str, amount:int):
    self.back.setdefault(item,0)
    self.back[item] += amount
  def cost(self, item:str,amount:int):
    if item != "鎊":
      try:
        if self.back[item] < amount:
          return False
        self.back[item] -= amount
        self.save()
        return True
      except:
        return False
    elif item == "鎊":
      if self.money < amount:
        return False
      self.money -= amount
      self.save()
      return True
    elif item not in self.back:
      return False