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


# ファイル名取得
def get_file_names(gcs_path):
  import tensorflow as tf
 
  for fn in tf.gfile.ListDirectory(gcs_path):
    yield {'gcs_path':gcs_path, 'filename':fn}


# 画像をGCSからロード
def load_image(element):
  import tensorflow as tf
  import numpy as np
  from PIL import Image
  
  # 画像のロード
  gcs_fn = element['gcs_path'] + '/' + element['filename']
  f = tf.gfile.Open(gcs_fn)
  im = Image.open(f)
  
  # 画像の切り取り
  im = im.crop((150, 100, 550, 500))

  # 画像の縮小（リサイズ）
  im = im.resize((256, 256))
 
  return {'filename': element['filename'],
          'img': im}


def save_to_gcs(element, gcs_path):
  import tensorflow as tf
  from PIL import Image
  
  gcs_fn = gcs_path + '/' + element['filename']
  f = tf.gfile.Open(gcs_fn, mode='w')
  
  element['img'].save(f)

p = beam.Pipeline(options=options)
(p | 'gcs_path' >> beam.Create(['gs://PROJECTID/images'])
   | 'get file names' >> beam.FlatMap(get_file_names)
   | 'load image' >> beam.Map(load_image)
   | 'save to gcs' >> beam.Map(save_to_gcs, 'gs://PROJECTID/output')
)
p.run().wait_until_finish()
