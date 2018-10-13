# Chapter 4
サンプルコードを実行する前に・・
- ソースコード中の `PROJECTID` を、自身のプロジェクトIDに変更してください
- [Dataflowを有効](https://console.cloud.google.com/apis/library/dataflow.googleapis.com)にしてください

サンプルコード実行前に `virtualenv` を設定します。
1. `virtualenv` コマンドを実行
```
$ virtualenv
```
2. `activate` を実行し、独立したPython環境を有効にする
```
$ source bin/activate
```
3. 必要なライブラリをインストールする
```
$ pip install -r requirements.txt
```

通常の環境に戻るには
```
$ deactivate
```
を実行します。
以降、Chapter 4 のサンプルコード実行前には
```
$ source bin/activate
```
を実行します。
