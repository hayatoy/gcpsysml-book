# -*- coding: utf-8 -*-

import apache_beam as beam

# プロジェクトID
PROJECTID = 'PROJECTID'

# オプション設定
options = beam.options.pipeline_options.PipelineOptions()

# GCP関連オプション
gcloud_options = options.view_as(
  beam.options.pipeline_options.GoogleCloudOptions)
gcloud_options.project = PROJECTID

# 標準オプション（実行環境を設定）
std_options = options.view_as(
  beam.options.pipeline_options.StandardOptions)
std_options.runner = 'DirectRunner'

p = beam.Pipeline(options=options)

query = "SELECT * " \
"FROM `bigquery-public-data.samples.shakespeare`" \
"LIMIT 10"

def upper_elem(element):
  corpus = element['corpus'].upper()
  word = element['word'].upper()
  return {'u_corpus': corpus, 'u_word': word}

def capitalize_elem(element):
  corpus = element['corpus'].capitalize()
  word = element['word'].capitalize()
  return {'c_corpus': corpus, 'c_word': word}

  
query_results = p | 'read' >> beam.io.Read(beam.io.BigQuerySource(
                                             project=PROJECTID,
                                             use_standard_sql=True,
                                             query=query))

# BigQueryの結果を二つのブランチに渡す
branch1 = query_results | 'upper' >> beam.Map(upper_elem)
branch2 = query_results | 'capitalize' >> beam.Map(capitalize_elem)

# ブランチからの結果をFlattenでまとめる
((branch1, branch2) | beam.Flatten()
                    | beam.io.WriteToText('gs://{}/p3.txt'.format(PROJECTID),
                                          num_shards=1)
)

p.run().wait_until_finish()
