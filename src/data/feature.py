#-*-coding:UTF-8-*-
'''
Created on 2018��8��28��
@author: mipapapa
'''
import numpy as np
import cv2

N_SEMATIC_CLASS = 10

class Feature:
    """ ��������ָ�ͼ�����ȡѶϢ, ��ǰ֡
    Attribes: 
        d: float,������̼��ۻ�����
        theta: float,��������Ƕ�
        h_l: array, ����ͼ����ಿ��ֱ��ͼ����
        h_c: array, ����ͼ���м䲿��ֱ��ͼ����
        h_r: array, ����ͼ���Ҳಿ��ֱ��ͼ����
    """
    def __init__(self):
        self.d = 0
        self.theta = 0
        self.h_l = np.zeros((N_SEMATIC_CLASS))
        self.h_c = np.zeros((N_SEMATIC_CLASS))
        self.h_r = np.zeros((N_SEMATIC_CLASS))
    
    def parse(self, pose, semantic_img):
        """
        ��һ������ָ�ͼ�񼰶�Ӧλ�ã�����Ϊ����ֵ
        Params:
            pose: LocPose, ����6���ɶ�λ����Ϣ
            sematic_img: ndarray2D: ����ָ���ͼ�񣨲���Readme_deeploc��
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
    k = 2   # ��������
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

