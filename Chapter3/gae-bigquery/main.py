# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from google.cloud import bigquery
import logging


# アプリケーションの作成
app = Flask(__name__)

# 各URIのハンドラを定義
@app.route('/')
def hello():
  return "Hello world!"

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

# HTTP POSTでデータを受け取る
@app.route('/post', methods=['POST'])
def city_post():
  city = request.form['city']
  address = request.form['address']
  
  insert_to_bigquery(city, address)
  
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
  