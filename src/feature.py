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

    
    def __repr__(self):
        return "%2.3f m, %2.3f d %2.2f  %2.2f" % (self.d, np.rad2deg(self.theta), self.x, self.y)
    
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
    
    def __add__(self, other):
        """ addition of two featues
        """
        new_feat = Feature()
        new_feat.d = self.d + other.d
        ta = self.d*np.sin(self.theta) + other.d*np.sin(other.theta)
        tb = self.d*np.cos(self.theta) + other.d*np.cos(other.theta)

#         new_feat.theta = np.arctan(ta/tb)    # 原文版本角度融合公式（-90~90）

        tn = np.sqrt(ta**2 + tb**2)
        ta = ta / tn
        tb = tb / tn
        tb = np.clip(tb, -1.0, 1.0)
        new_feat.theta = np.arccos(tb) * (-1.0 if ta < 0 else 1.0)

        new_feat.h_l = (self.d * self.h_l + other.d * other.h_l) / (self.d + other.d)
        new_feat.h_c = (self.d * self.h_c + other.d * other.h_c) / (self.d + other.d)
        new_feat.h_r = (self.d * self.h_r + other.d * other.h_r) / (self.d + other.d)
        
        # 使用右值的坐标作为新特征的坐标
        new_feat.x = other.x
        new_feat.y = other.y
        
        return new_feat
    
    def __sub__(self, other):
        """ distance of two featues
        """
        d_h_l = 1. - np.dot(self.h_l, other.h_l) / (np.sqrt(np.sum(self.h_l**2) * np.sum(other.h_l**2)))
        d_h_c = 1. - np.dot(self.h_c, other.h_c) / (np.sqrt(np.sum(self.h_c**2) * np.sum(other.h_c**2)))
        d_h_r = 1. - np.dot(self.h_r, other.h_r) / (np.sqrt(np.sum(self.h_r**2) * np.sum(other.h_r**2)))
        return np.max([d_h_l, d_h_c, d_h_r])
    
    def __mod__(self, other):
        """ 计算角度差绝对值
            返回角度值
        """
        r = np.cos(self.theta)*np.cos(other.theta)+np.sin(self.theta)*np.sin(other.theta)
        r = np.clip(r, -1.0, 1.0)
        return np.rad2deg(np.arccos(r))
    
    def copy(self, other):
        self.theta = other.theta
        self.x = other.x
        self.y = other.y
        self.h_l[:] = other.h_l[:]
        self.h_c[:] = other.h_c[:]
        self.h_r[:] = other.h_r[:]
        self.d = other.d
        
    
def load_label_img(png_path):
    """ 读入一副语义分割图片，将其中像素解析为等分3个区域的语义统计直方图
        reference：Readme_deeploc
    """
    sem_img = cv2.imread(png_path)[:,:,0]
    h, w = sem_img.shape
    ww = int(w/3)
    k = 3   # 采样步长
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
#     png_path = r"F:\dataset\DeepLoc\semantic\ts_seq1\labels\Image_1.png"
#     hist_l, hist_c, hist_r = load_label_img(png_path)
    f1 = Feature()
    f1.d = 1
    f1.theta = np.deg2rad(-90)
    
    f2 = Feature()
    f2.d = 1
    f2.theta = np.deg2rad(-90)
    
    f3 = f1 + f2
    print(f1)
    print(f2)
    print(f3)

    
if __name__=="__main__":
    pass
    main()






