#-*-coding:UTF-8
'''
Created on 2018年9月6日
@author: mipapapa
基于TSM与PF进行定位
'''
from feature import Feature
from dataset import load_feature_npy
from sem_map import TSM, SemaObservation
from display import plotTSM
from vehicle import Vehile


def main():
    # 建立全局语义地图GTSM
    feature_tsm = load_feature_npy(r"dataset/ts_seq1_feature.npy")
    gtsm = TSM()
    sov = SemaObservation()
    for t in range(len(feature_tsm)):
        Ft = feature_tsm[t]
        fso = sov.input(Ft)
        gtsm.mapping(fso)
    gtsm.close_looping()
#     plotTSM(tsm)

    # 载入观测数据，基于车辆模型（观测，更新，评估）与粒子滤波器进行位置迭代更新
    feature_loc = load_feature_npy(r"dataset/ts_seq1_feature.npy")
    
    myrobot = Vehile()
    
    for t in range(len(feature_loc)):
        Ft = feature_loc[t]
        Z = myrobot.sense(Ft)
        
    
    
if __name__=="__main__":
    pass
    main()

