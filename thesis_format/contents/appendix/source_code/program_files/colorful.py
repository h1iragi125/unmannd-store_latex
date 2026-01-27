import cv2
import numpy as np
import csv

target_zones = []
# プログラム利用の際，"csv_data"は画像内商品のデータを入力したcsvファイルを用いる
with open("csv_data", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        label = row['label']
        color_B = int(row['color_B'])
        color_G = int(row['color_G'])
        color_R = int(row['color_R'])
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        h_min = int(row['h_min'])
        h_max = int(row['h_max'])
        s_min = int(row['s_min'])
        s_max = int(row['s_max'])
        v_min = int(row['v_min'])
        v_max = int(row['v_max'])
        target_zones.append({"label": label, "rect": (x1,y1,x2,y2), "color": (color_B,color_G,color_R), "hsv":((h_min, s_min, v_min), (h_max, s_max, v_max))})

# プログラム利用の際，"image"は実際の画像を入れる
img = cv2.imread('image/kurisu_bakery.jpg') 

# サイズ調整
scale_percent = 20
w = int(img.shape[1]*scale_percent/100)
h = int(img.shape[0]*scale_percent/100)
r = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

r_color = cv2.cvtColor(r, cv2.COLOR_BGR2HSV) # カラー変換

for zone in target_zones: # 商品判定に用いる範囲の可視化
    x1, y1, x2, y2 = zone['rect']
    # 各商品ごとにしきい値設定
    lower, upper = np.array(zone['hsv'])
    cv2.rectangle(r_color, (x1,y1), (x2,y2), zone['color'], 2)
    cv2.putText(r_color, zone['label'], (x1,y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, zone['color'], 1)

mask = cv2.inRange(r_color, lower, upper) # 単体mask（閾値のトレードオフが起こらないとき）
result = cv2.bitwise_and(r_color, r_color, mask=mask)

contours, _ =cv2.findContours(mask, 
                              cv2.RETR_EXTERNAL,  # 外側の輪郭
                              cv2.CHAIN_APPROX_SIMPLE) # 直線近似

min_area = 580 # 面積が小さい輪郭指定
max_area = 3000 # 面積が大きい輪郭指定
target_counts = {zone['label']: 0 for zone in target_zones}

for i, contour in enumerate(contours): # 明度が高い部分（白い部分）の座標抽出 
    area = cv2.contourArea(contour) # 面積小さい輪郭削除
    if area < min_area:
        continue
    if area > max_area:
        continue
    x, y, w, h = cv2.boundingRect(contour)
    cx = x+(w/2)
    cy = y+(h/2)
    # print(f"領域{i}: center=({cx},{cy}), width={w}, height={h}")
 
    # 判定
    judged_label = None
    judged_color = (255,0,0)
    for zone in target_zones:
        x1, y1, x2, y2 = zone['rect']
        if x1 <= cx <= x2 and y1 <= cy <= y2: 
            judged_label = zone['label']
            judged_color = zone['color']
            target_counts[judged_label] += 1
            break

    if judged_label is not None:
        # 判定に用いたバウンディングボックス表示
        cv2.rectangle(r_color, (x,y), (x+w, y+h),
                          judged_color, # 描画の色（Blue, Green, Red）
                          2 # 描画の線の太さ
                          )

        # バウンディングボックスの中心座標表示
        cv2.circle(r_color, (int(cx),int(cy)),
                   3, # 円の半径 
                   (0,255,255),
                   -1 # 線の太さ（-1は塗りつぶし指定）
                   )

        # ラベル表示
        cv2.putText(r_color, judged_label, (x,y-5), # テキストの座標
                    cv2.FONT_HERSHEY_SIMPLEX, # フォント
                    0.5, # フォントサイズ（倍率）
                    judged_color,
                    1 # 線の太さ
                    )

# 商品の個数表示(ターミナル)
for label, count in target_counts.items():
    number = f"{label}: {count}"
    print(f"{label}: {count} 個")

cv2.imshow('Original', r_color) 
cv2.waitKey(0)
cv2.destroyAllWindows()