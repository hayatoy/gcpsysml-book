# Chapter3
Cloud Shell 上で各サブフォルダに移動し、以下のコマンドを実行します。

** ローカル(Cloud Shell上)でアプリを起動 **
```
$ dev_appserver.py app.yaml
```
** GAE 環境上でアプリを起動 **
```
$ gcloud app deploy --version=testver
```

## 3-2-2 GAE アプリケーションの作成

`/gae-hello`

## 3-2-4 Datastore への保存

`/gae-datastore`

## 3-3-2 BigQuery API の利用
[BigQuery API の有効化を確認](https://console.cloud.google.com/apis/api/bigquery-json.googleapis.com/overview)

`./make_dataset.py` および `./make_table.py` を先に実行します。
エラーが発生する場合は以下を実行
```
$ pip install --upgrade google-cloud-bigquery --user
```

以下に移動してデプロイします。  
`/gae-bigquery`

## 3-4 Firebase
先に[Firebase Console](https://console.firebase.google.com/)でプロジェクトを作成します。

以下に移動してデプロイします。  
`/gae-firebase`



