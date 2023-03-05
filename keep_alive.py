from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return "<body style='background:black;color:teal;'><h1>I'm keeping everything alive so come and join me uwu <3</h1></body>"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()
