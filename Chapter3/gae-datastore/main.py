# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from google.appengine.ext import ndb
import logging

class CityAddress(ndb.Model):
  city = ndb.StringProperty()
  address = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now=True)

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
  
  # Datastoreへ書き込み
  entity = CityAddress(city=city, address=address)
  entity.put()
  
  return u"City: {},\nAddress: {}\n".format(city, address)

@app.route('/list', methods=['GET'])
def city_list():
  query = CityAddress.query().order(-CityAddress.date)  # date 降順ソート
  entities = query.fetch(10)                            # 10件フェッチ
  list_latest = [e.to_dict() for e in entities]         # Dictに変換
  return jsonify(list_latest)                           # JSON形式で返す
  