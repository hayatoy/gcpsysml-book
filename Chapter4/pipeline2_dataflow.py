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
gcloud_options.job_name = 'pipeline2'
gcloud_options.staging_location = 'gs://{}/staging'.format(PROJECTID)
gcloud_options.temp_location = 'gs://{}/temp'.format(PROJECTID)

# 標準オプション（実行環境を設定）
std_options = options.view_as(
  beam.options.pipeline_options.StandardOptions)
std_options.runner = 'DataflowRunner'

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
   | 'upper' >> beam.Map(upper_elem)
   | 'write' >> beam.io.WriteToText('gs://{}/p2.txt'.format(PROJECTID),
                                    num_shards=1)
)

p.run()
