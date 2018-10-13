# -*- coding: utf-8 -*-
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

# クライアントライブラリを初期化
credentials = GoogleCredentials.get_application_default()
ml = discovery.build('ml', 'v1', credentials=credentials)

PROJECTID = 'PROJECTID'
JOBID = 'simplejob_api1'
GCS_PATH = 'gs://PROJECTID/simplejob/trainer-0.0.0.tar.gz'

# 学習ジョブの設定
job_req = ml.projects().jobs().create(
  parent='projects/' + PROJECTID,
  body={'jobId': JOBID,
        'trainingInput': {'scaleTier': 'BASIC',
                          'packageUris': [GCS_PATH],
                          'pythonModule': 'trainer.task',
                          'region': 'us-central1',
                          'runtimeVersion': '1.7'
                          }
        }
)

# 学習ジョブの実行
response = job_req.execute()
print(response)