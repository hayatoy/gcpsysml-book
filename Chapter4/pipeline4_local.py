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
"FROM `bigquery-public-data.samples.shakespeare`" #\
#"LIMIT 100"


def make_kvpair(element):
  k = element['word'][0].lower()
  v = 1
  return (k, v)

def count_ones(kvpair):
  return (kvpair[0], sum(kvpair[1]))

(p | 'read' >> beam.io.Read(beam.io.BigQuerySource(
                                             project=PROJECTID,
                                             use_standard_sql=True,
                                             query=query))
   | 'pair' >> beam.Map(make_kvpair)
   | 'groupby' >> beam.GroupByKey()
   | 'count' >> beam.Map(count_ones)
   | 'write' >> beam.io.WriteToText('gs://{}/p4.txt'.format(PROJECTID),
                                    num_shards=1)
)

p.run().wait_until_finish()
