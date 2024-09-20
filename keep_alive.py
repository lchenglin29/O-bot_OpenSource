from flask import Flask, request
from threading import Thread
from objects.player_object import players
from mydef.mydef import load_json
app = Flask('')

@app.route('/',methods=['GET'])
def main():
  return '嗚呼我上線囉'

@app.route('/change_user_data',methods=['POST'])
def change_user_data():
  dict = request.get_json()
  player = players(str(dict['user_id']))
  player.change_money(dict['money'])
  player.save()
  return 'ok'

@app.route('/user_data',methods=['POST'])
def user_data():
  dict = request.get_json()
  data = load_json()
  user_data = data[str(dict['user_id'])]
  return user_data

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()