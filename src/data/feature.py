#-*-coding:UTF-8
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
        self.d = 0      # 最近的累积里程数(M)
        self.theta = 0  # 当前车辆朝向(RAD)
        self.h_l = np.zeros((N_SEMATIC_CLASS))  # 左侧语义直方图
        self.h_c = np.zeros((N_SEMATIC_CLASS))  # 中侧语义直方图
        self.h_r = np.zeros((N_SEMATIC_CLASS))  # 右侧语义直方图
        
        self.x = 0      # 自车X坐标
        self.y = 0      # 自车Y坐标
        
    def parse(self, pose, hist_l, hist_c, hist_r, acc_veh_odm):
        """
        将一幅语义分割直方图及对应位置，解析为特征值
        Params:
            pose: LocPose, 车辆6自由度位姿信息
            img_l, img_c, img_r: ndarray1D: 语义直方图（使用load_label_img获得）
            acc_veh_odm: 从起始到当前帧的累积里程计(m)
        """
        self.theta = pose.data[3]
        self.x = pose.data[0]
        self.y = pose.data[1]
        
        self.h_l[:] = hist_l[:]
        self.h_c[:] = hist_c[:]
        self.h_r[:] = hist_r[:]
        
        self.d = acc_veh_odm
        
def load_label_img(png_path):
    """ 读入一副语义分割图片，将其中像素解析为等分3个区域的语义统计直方图
        reference：Readme_deeploc
    """
    sem_img = cv2.imread(png_path)[:,:,0]
    h, w = sem_img.shape
    ww = int(w/3)
    k = 2   # 采样步长
    new_szie = int(h * ww / (k*k) )
    img_l = np.reshape(sem_img[::k,  0:ww:k], (new_szie))
    img_c = np.reshape(sem_img[::k,  ww:2*ww:k], (new_szie))
    img_r = np.reshape(sem_img[::k,  2*ww:3*ww:k], (new_szie))
    
    hist_l = np.zeros((N_SEMATIC_CLASS), np.uint32)
    hist_c = np.zeros((N_SEMATIC_CLASS), np.uint32)
    hist_r = np.zeros((N_SEMATIC_CLASS), np.uint32)
    
    for i in range(new_szie):
        hist_l[img_l[i]] += 1
        hist_c[img_c[i]] += 1
        hist_r[img_r[i]] += 1
    return hist_l, hist_c, hist_r
    
def main():
    png_path = r"F:\dataset\DeepLoc\semantic\ts_seq1\labels\Image_1.png"
    hist_l, hist_c, hist_r = load_label_img(png_path)
    
if __name__=="__main__":
    pass
    main()









