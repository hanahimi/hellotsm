#-*-coding:UTF-8-*-
'''
Created on 2018年8月28日
@author: mipapapa
'''
import numpy as np
import cv2

N_SEMATIC_CLASS = 10

class Feature:
    """ 单幅语义分割图像的提取讯息, 当前帧
    Attribes: 
        d: float,车辆里程计累积距离
        theta: float,车辆航向角度
        h_l: array, 语义图像左侧部分直方图特征
        h_c: array, 语义图像中间部分直方图特征
        h_r: array, 语义图像右侧部分直方图特征
    """
    def __init__(self):
        self.d = 0
        self.theta = 0
        self.h_l = np.zeros((N_SEMATIC_CLASS))
        self.h_c = np.zeros((N_SEMATIC_CLASS))
        self.h_r = np.zeros((N_SEMATIC_CLASS))
    
    def parse(self, pose, semantic_img):
        """
        将一幅语义分割图像及对应位置，解析为特征值
        Params:
            pose: LocPose, 车辆6自由度位姿信息
            sematic_img: ndarray2D: 语义分割结果图像（参照Readme_deeploc）
        """
        self.theta = pose.data[3]
        h, w = semantic_img.shape
        ww = int(w/3)
        img_l = semantic_img[:,  0:ww]
        img_c = semantic_img[:,  ww:2*ww]
        img_r = semantic_img[:,  2*ww:3*ww]
        

def load_label_img(png_path):
    sem_img = cv2.imread(png_path)[:,:,0]
    h, w = sem_img.shape
    ww = int(w/3)
    k = 2   # 采样步长
    new_szie = h * ww /(k*k)
    img_l = np.reshape(sem_img[::k,  0:ww:k], (new_szie))
    img_c = np.reshape(sem_img[::k,  ww:2*ww:k], (new_szie))
    img_r = np.reshape(sem_img[::k,  2*ww:3*ww:k], (new_szie))
    
    hist_l = np.zeros((N_SEMATIC_CLASS), np.float16)
    hist_c = np.zeros((N_SEMATIC_CLASS), np.float16)
    hist_r = np.zeros((N_SEMATIC_CLASS), np.float16)
    
    for i in range(new_szie):
        hist_l[img_l[i]] += 1
        hist_c[img_c[i]] += 1
        hist_r[img_r[i]] += 1
    return hist_l, hist_c, hist_r
    
def main():
    png_path = r"D:\Dataset\public_data\DeepLoc\train\labels\Image_1.png"
    load_label_img(png_path)
    
if __name__=="__main__":
    pass
    main()

