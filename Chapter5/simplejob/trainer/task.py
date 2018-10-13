# -*- coding: utf-8 -*-

# パッケージの読み込み
import tensorflow as tf
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

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

NUM_FEATURES = 30
NUM_UNITS_H1 = 4
NUM_UNITS_H2 = 4
NUM_CLASSES = 2

with tf.Graph().as_default():
  # 入力層
  X = tf.placeholder(tf.float32, shape=[None, NUM_FEATURES], name="X")
  y = tf.placeholder(tf.float32, shape=[None, ], name="y")

  # 隠れ層
  hidden1 = tf.layers.dense(inputs=X,
                            units=NUM_UNITS_H1,
                            activation=tf.nn.relu,
                            name='hidden1')
  hidden2 = tf.layers.dense(inputs=hidden1,
                            units=NUM_UNITS_H2,
                            activation=tf.nn.relu,
                            name='hidden2')

  # 出力層
  logits = tf.layers.dense(inputs=hidden2,
                           units=NUM_CLASSES,
                           name='output')

  # 損失
  onehot_labels = tf.one_hot(indices=tf.cast(y, tf.int32),
                             depth=NUM_CLASSES)
  cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
      labels=onehot_labels,
      logits=logits,
      name='xentropy')
  loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')

  # 損失を最小化
  train_op = tf.train.AdamOptimizer(0.01).minimize(loss)

  # テスト用の正解率演算オペレーション
  correct_prediction = tf.equal(tf.argmax(logits, 1),
                                tf.argmax(onehot_labels, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for step in range(1000):
      _, loss_value = sess.run([train_op, loss],
                               feed_dict={X: X_train, y: y_train})
      if step % 100 == 0:
        print('Step: %d, Loss: %f' % (step, loss_value))

    # テストデータで正解率を求める
    acc = sess.run(accuracy, feed_dict={X: X_test, y: y_test})
    print('Accuracy: %f' % acc)
