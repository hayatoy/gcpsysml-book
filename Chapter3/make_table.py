# -*- coding: utf-8 -*-
from google.cloud import bigquery

# クライアントのインスタンスを作成
client = bigquery.Client()

# データセットの参照
dataset_ref = client.dataset('chapter3')

# スキーマを作成
schema = [
  bigquery.SchemaField('city', 'STRING', mode='REQUIRED'),
  bigquery.SchemaField('address', 'STRING', mode='REQUIRED'),
]

# テーブルの参照
table_ref = dataset_ref.table('city_address')
table = bigquery.Table(table_ref, schema=schema)

# テーブルの作成 (APIリクエスト)
table = client.create_table(table)

print('Table {} created.'.format(table.table_id))