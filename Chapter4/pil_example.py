# -*- coding: utf-8 -*-

# PILのインポート
from PIL import Image

# JPEG画像のロード
im = Image.open("images/seagull.jpg")

# 画像の切り取り
im = im.crop((150, 100, 550, 500))

# 画像の縮小（リサイズ）
im = im.resize((256, 256))

# 切り取った画像の保存
im.save("gull_crop.jpg")