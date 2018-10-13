# -*- coding: utf-8 -*-
from google.cloud import bigquery

# クライアントのインスタンスを作成
client = bigquery.Client()

# データセットの参照を作成
dataset_ref = client.dataset('chapter3')
dataset = bigquery.Dataset(dataset_ref)

# 新しいデータセットを作成 (APIリクエスト)
dataset = client.create_dataset(dataset)

print('Dataset {} created.'.format(dataset.dataset_id))