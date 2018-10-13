# -*- coding: utf-8 -*-
from flask import Flask, request

# アプリケーションの作成
app = Flask(__name__)

def _dataflow_job_start():
  # 必要なライブラリをインポート
  from oauth2client.client import GoogleCredentials
  from oauth2client.service_account import ServiceAccountCredentials
  from apiclient.discovery import build
  
  # クライアントライブラリを初期化
  credentials = GoogleCredentials.get_application_default()
  service = build("dataflow", "v1b3", credentials=credentials)
  templates = service.projects().templates()

  # JOBの設定項目
  BODY = {
           "jobName": "Job from GAE",
           "gcsPath": "gs://PROJECTID/dftemplate",
           "environment": {
             "tempLocation": "gs://PROJECTID/temp",
           }
         }
  
  # JOBの実行
  dfrequest = service.projects().templates().create(
    projectId='PROJECTID', body=BODY)
  return dfrequest.execute()
  
# Cronで呼ばれるURLのハンドラ
@app.route('/dfstart')
def dataflow_job_start():
  
  _dataflow_job_start()
  return
