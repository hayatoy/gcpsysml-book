# -*- coding: utf-8 -*-
from flask import Flask, request

# アプリケーションの作成
app = Flask(__name__)

# 各URIのハンドラを定義
@app.route('/')
def hello():
  return "Hello world!"

# HTTP POSTでデータを受け取る
@app.route('/post', methods=['POST'])
def city_post():
  city = request.form['city']
  address = request.form['address']
  
  return u"City: {},\nAddress: {}\n".format(city, address)

