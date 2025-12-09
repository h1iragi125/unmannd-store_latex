import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
from tensorflow.keras.optimizers import Adagrad
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from PIL import Image
import os
import re
import matplotlib.pyplot as plt

#画像を読み込む
def list_pictures(directory, ext='jpg|jpeg|bmp|png|ppm'):
    return [os.path.join(root, f)
            for root, _, files in os.walk(directory) for f in files
            if re.match(r'([\w]+.(?:' + ext + '))', f.lower())]

X = []
Y = []
#0人の画像
for picture in list_pictures('./train_picture/zero/'):
    img = img_to_array(load_img(picture, target_size=(24,32)))
    X.append(img)
    Y.append(0)
#1人の画像
for picture in list_pictures('./train_picture/one/'):
    img = img_to_array(load_img(picture, target_size=(24,32)))
    X.append(img)
    Y.append(1)
#2人の画像
for picture in list_pictures('./train_picture/two/'):
    img = img_to_array(load_img(picture, target_size=(24,32)))
    X.append(img)
    Y.append(2)
#3人の画像
for picture in list_pictures('./train_picture/three/'):
    img = img_to_array(load_img(picture, target_size=(24,32)))
    X.append(img)
    Y.append(3)
# arrayに変換
X = np.asarray(X)
Y = np.asarray(Y)
# 画素値を0から1の範囲に変換
X = X.astype('float32')
X = X / 255.0
# クラスの形式を変換
Y = to_categorical(Y)
# 学習用データとテストデータに分ける
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=111)

# モデルの構築
model = Sequential()
model.add(keras.layers.Conv2D(16, (3, 3), padding='same',input_shape=X_train.shape[1:])) # 畳み込み層
model.add(Activation('relu')) # 活性化関数
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2))) # プーリング層

model.add(keras.layers.Conv2D(32, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten()) # 二次元データを一次元データに変換
model.add(Dense(512)) # 全結合層
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(4))       # クラスは4個
model.add(Activation('softmax')) # ソフトマックス関数

# モデルをコンパイル
model.compile(loss="categorical_crossentropy", # 損失関数 交差エントロピー誤差
              optimizer='adam', # 最適化アルゴリズム ADAM
              metrics=["accuracy","Precision","Recall","F1Score"]) # 評価指数 正答率、適合率、再現率、F1Score
es_cb=keras.callbacks.EarlyStopping(monitor='val_loss',mode='auto')# EarlyStopping 

# 学習を実行
history=model.fit(X_train, y_train, epochs=200,validation_data = (X_test, y_test),callbacks=es_cb)

# テストデータを予測
predict_prob=model.predict(X_test)
predict_classes=np.argmax(predict_prob,axis=1)

# 混合行列の作成
mg_df = pd.DataFrame({'predict': predict_classes, 
                      'class': np.argmax(y_test, axis=1)})
pd.crosstab(mg_df['class'], mg_df['predict'])

# 評価指数を表示
score = model.evaluate(X_test,y_test,verbose=1)
print('Test loss:',score[0])
print('Test Accuracy:', score[1])
print('Test Precision:', score[2])
print('Test Recall:', score[3])
print('Test F1Score:', score[4])

pd.crosstab(mg_df['class'], mg_df['predict'])
