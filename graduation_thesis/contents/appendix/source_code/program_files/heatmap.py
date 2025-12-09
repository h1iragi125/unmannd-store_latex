import matplotlib.pyplot as plt     # pip install matplotlib
import numpy as np                  # pip install numpy
import os
import glob
import cv2

# データの保存先を作成
input_dir_path = "./input"
os.makedirs(input_dir_path, exist_ok=True)
output_dir_path = "./output"
os.makedirs(output_dir_path, exist_ok=True)
os.makedirs(output_dir_path + "/thermalmap", exist_ok=True)

def CountContours(impath):
    cvimg=cv2.imread(impath)
    bigimg=cv2.resize(cvimg,None,fx=20,fy=20, interpolation=cv2.INTER_NEAREST)
    grayimg=cv2.cvtColor(cvimg,cv2.COLOR_BGR2GRAY)
    blurimg=cv2.blur(grayimg,(3,3)) #平滑化
    blurimg=cv2.resize(blurimg,None,fx=20,fy=20, interpolation=cv2.INTER_NEAREST)
    ret,dst = cv2.threshold(blurimg,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours,hierarchy=cv2.findContours(dst,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    #輪郭抽出
    img_result = cv2.drawContours(bigimg, contours, -1, (0, 0, 255), 2)
    print("輪郭数："+str(len(contours)))
    cv2.imshow("IMAGE", img_result) #輪郭を描きこんだ画像を表示
    cv2.waitKey()
    
            
        
for f in glob.glob(input_dir_path + "/*.csv"):  #赤外線画像データ読み込み
    csv_file_name = os.path.split(f)[1]
    date_str = csv_file_name[:-4]
    thermal_data = np.loadtxt(input_dir_path + '/' + csv_file_name, delimiter=',')
    fig, ax = plt.subplots(figsize=thermal_data.shape[::-1],dpi=1, tight_layout=True)
    ax.imshow(thermal_data, cmap="gist_gray")    #グレースケール：gist_gray カラー:jet
    ax.axis("off")
    fig.savefig(output_dir_path + "/thermalmap/" + date_str + ".png",dpi=1)
    plt.close()
    impath=output_dir_path + "/thermalmap/" + date_str + ".png"
    CountContours(impath)