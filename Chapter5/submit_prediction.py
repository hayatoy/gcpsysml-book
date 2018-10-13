# -*- coding: utf-8 -*-
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# 乳がんのデータをロード
X_dataset, y_dataset = load_breast_cancer(return_X_y=True)

# X_datasetをX_trainとX_testに
# y_datasetをy_trainとy_testに分割
X_train, X_test, y_train, y_test = train_test_split(
  X_dataset, y_dataset, test_size=0.2, random_state=42)

# データを0~1の範囲にスケール
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ラベルデータをone-hot形式に変換
enc = OneHotEncoder(sparse=False)
y_test = enc.fit_transform(y_test.reshape(-1, 1))

from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

credentials = GoogleCredentials.get_application_default()
ml = discovery.build('ml', 'v1', credentials=credentials)

PROJECTID = 'PROJECTID'
MODELNAME = 'cancer'

project_id = 'projects/{}'.format(PROJECTID)
model_id = '{}/models/{}'.format(project_id, MODELNAME)

request_body = {'instances': [{'input': list(X_test[0])},
                              {'input': list(X_test[1])},
                              {'input': list(X_test[2])},
                              {'input': list(X_test[3])}
                              ]}

request = ml.projects().predict(name=model_id, body=request_body)
response = request.execute()
print(response)