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
  element['corpus'] = element['corpus'].upper()
  element['word'] = element['word'].upper()
  return element

(p | 'read' >> beam.io.Read(beam.io.BigQuerySource(project=PROJECTID,
                                                   use_standard_sql=True,
                                                   query=query))
   | 'modify' >> beam.Map(upper_elem)
   | 'write' >> beam.io.WriteToText('gs://{}/p2.txt'.format(PROJECTID),
                                    num_shards=1)
)

p.run().wait_until_finish()
