# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from google.cloud import bigquery
import firebase_admin
from firebase_admin import db
from google.appengine.api.app_identity import get_application_id
import logging

# アプリケーションの作成
app = Flask(__name__)

# 各URIのハンドラを定義
@app.route('/')
def main_page():
  params = {'app_id': get_application_id()}
  return render_template("main.html", **params)

# BigQueryへのストリーミングインサート
def insert_to_bigquery(city, address):
  # クライアントのインスタンスを作成
  client = bigquery.Client()
  
  # データセットの参照
  dataset_ref = client.dataset('chapter3')
  
  # テーブルの参照 (APIリクエスト)
  table_ref = dataset_ref.table('city_address')
  table = client.get_table(table_ref)
  
  # 行データのインサート (APIリクエスト)
  rows_to_insert = [(city, address)]
  client.insert_rows(table, rows_to_insert)


# Firebase Realtime Databaseへライト
def insert_to_firebase(city, address):
  try:
    firebase_admin.get_app()
  except ValueError:
    app_id = get_application_id()
    firebase_admin.initialize_app(options={
      'databaseURL': 'https://{}.firebaseio.com'.format(app_id)
    })
  
  kv_to_insert = {'city': city,
                  'address': address,
                  'time': {'.sv': 'timestamp'}
                 }
  ref = db.reference('city-address/latest')
  ref.update(kv_to_insert)
  

# HTTP POSTでデータを受け取る
@app.route('/post', methods=['POST'])
def city_post():
  city = request.form['city']
  address = request.form['address']
  
  insert_to_bigquery(city, address)
  insert_to_firebase(city, address)
  
  return u"City: {},\nAddress: {}\n".format(city, address)


# BigQueryのデータをリスト表示
@app.route('/list', methods=['GET'])
def city_list():
  QUERY = (
    'SELECT'
    '  *'
    'FROM'
    '  `PROJECTID.chapter3.city_address`'
    'WHERE'
    '  city = "osaka"'
    'ORDER BY'
    '  address DESC'
  )
  TIMEOUT = 30  # 秒
  
  # クライアントのインスタンスを作成
  client = bigquery.Client()
  
  # クエリのスタート
  query_job = client.query(QUERY)
  
  # クエリが終了するのを待つ
  iterator = query_job.result(timeout=TIMEOUT)
  
  # JSON形式で返す
  list_latest = [dict(r) for r in iterator]
  return jsonify(list_latest)
  