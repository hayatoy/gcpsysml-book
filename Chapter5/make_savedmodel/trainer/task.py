# -*- coding: utf-8 -*-

# パッケージの読み込み
import tensorflow as tf
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import utils
from tensorflow.python.keras import losses
from tensorflow.python.keras import optimizers
from tensorflow.python.keras import backend

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
y_train = utils.to_categorical(y_train, 2)
y_test = utils.to_categorical(y_test, 2)

NUM_FEATURES = 30
NUM_UNITS_H1 = 4
NUM_UNITS_H2 = 4
NUM_CLASSES = 2

# Sequentialモデルで線形に積み重ねる
model = Sequential()
model.add(Dense(units=NUM_UNITS_H1, activation='relu', input_dim=NUM_FEATURES))
model.add(Dense(units=NUM_UNITS_H2, activation='relu'))
model.add(Dense(units=NUM_CLASSES, activation='softmax'))

model.compile(loss=losses.categorical_crossentropy,
              optimizer=optimizers.Adam(),
              metrics=['accuracy'])

# 学習を実行
model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=2)


# 入出力のTensorを取得
x = model.input
y = model.output

# 入出力Tensor情報を作成
inputs = {"input": tf.saved_model.utils.build_tensor_info(x)}
outputs = {"output": tf.saved_model.utils.build_tensor_info(y)}

# SignatureDefを作成
signature = tf.saved_model.signature_def_utils.build_signature_def(
  inputs=inputs,
  outputs=outputs,
  method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
)

# SavedModelを作成
sess = backend.get_session()
b = tf.saved_model.builder.SavedModelBuilder(
      'gs://[BUCKET]/simplekerasjob/savedmodel')
b.add_meta_graph_and_variables(sess,
                               [tf.saved_model.tag_constants.SERVING],
                               signature_def_map={
                                 'serving_default': signature})
b.save()