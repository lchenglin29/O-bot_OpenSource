import json,datetime,pytz
import discord
import random

def load_json():
  with open('data/data.json', mode='r', encoding="utf8") as jFile:
      jdata = json.load(jFile)
  #print(jdata)
  jFile.close()
  return jdata

def write_js(data):
  jsdata = json.dumps(data,ensure_ascii=False)
  with open('data/data.json', mode='w', encoding="utf8") as jFile:
    jFile.write(jsdata)
    jFile.close()

def load_item_data():
  with open('data/items_data.json', mode='r', encoding="utf8") as jFile:
      jdata = json.load(jFile)
  #print(jdata)
  jFile.close()
  return jdata

def write_item_data(data):
  jsdata = json.dumps(data,ensure_ascii=False)
  with open('data/items_data.json', mode='w', encoding="utf8") as jFile:
    jFile.write(jsdata)
    jFile.close()

def load_bank_data():
  with open('data/bank_data.json', mode='r', encoding="utf8") as jFile:
      jdata = json.load(jFile)
  #print(jdata)
  jFile.close()
  return jdata

def write_bank_data(data):
  jsdata = json.dumps(data,ensure_ascii=False)
  with open('data/bank_data.json', mode='w', encoding="utf8") as jFile:
    jFile.write(jsdata)
    jFile.close()

def load_company_data():
  with open('data/company_data.json', mode='r', encoding="utf8") as jFile:
      jdata = json.load(jFile)
  #print(jdata)
  jFile.close()
  return jdata

def write_company_data(data):
  jsdata = json.dumps(data,ensure_ascii=False)
  with open('data/company_data.json', mode='w', encoding="utf8") as jFile:
    jFile.write(jsdata)
    jFile.close()

def now_time():
    current_time = datetime.datetime.now()
    timezone = pytz.timezone('Asia/Taipei')
    localized_time = current_time.astimezone(timezone)
    return localized_time.strftime("%Y-%m-%d %H:%M")

def now_data():
  taipei_timezone = pytz.timezone('Asia/Taipei')
  current_date = datetime.datetime.now(taipei_timezone).date()
  print("臺灣的當前日期:", current_date)
  return str(current_date)

def textmsg(user):
  return f'回覆:{user} | 時間:{now_time()}'

def generate_secret_number():
    return ''.join(random.sample('0123456789', 4))

def evaluate_guess(secret, guess):
    a_count = sum([1 for s, g in zip(secret, guess) if s == g])
    b_count = sum([1 for digit in set(guess) if digit in secret]) - a_count
    return f'{a_count}A{b_count}B'
