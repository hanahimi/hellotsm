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
from vehicle import Vehile, eval_particals
from partical_filter import ParticalFilter

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def main():
    
    # 建立全局语义地图GTSM
    feature_tsm = load_feature_npy(r"dataset/tr_seq1_feature.npy")
    gtsm = TSM()
    sov = SemaObservation(nf=5, feat_dist=0.2, orient_diff_ths=10)
    
    for t in range(len(feature_tsm)):
        Ft = feature_tsm[t]
        fso, nfuse = sov.input(Ft)
        gtsm.mapping(fso, nfuse)
    gtsm.close_looping()
    plotTSM(gtsm)

    # 载入观测数据，基于车辆模型（观测，更新，评估）与粒子滤波器进行位置迭代更新
    feature_loc = load_feature_npy(r"dataset/ts_seq1_feature.npy")
     
    real_car = Vehile(len(gtsm.edges))      # 随机设置车的位置
    real_car.set(0, 0.908921146195)
#     real_car.set_noise(0.)
     
    filter = ParticalFilter(1000)
     
    for _i in range(filter.N):
        new_obj = Vehile(len(gtsm.edges))
        new_obj.set_noise(0.4)
        filter.p.append(new_obj)
     
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ion()
    main_time = 0
    while main_time < 10:
        main_time += 1
          
        for t in range(len(feature_loc)):
            Ft = feature_loc[t]
            forward_distance = Ft.d
            real_car = real_car.move(forward_distance, gtsm)
            Z = real_car.sense(Ft)
            plt.clf()
              
            for i in range(len(gtsm.nodes)):
                node = gtsm.nodes[i]
                plt.scatter(node.x, node.y, s=10, alpha=0.3)

#             r_x, r_y, r_t = real_car.loc(gtsm)
#             plt.plot(r_x, r_y, "bo")

            p_predict = []
            p_x_s, p_y_s, s_s = [], [], []
            for i in range(filter.N):
                tmp_p = filter.p[i].move(forward_distance, gtsm)
                p_x, p_y, p_t = tmp_p.loc(gtsm)
                p_x_s.append(p_x)
                p_y_s.append(p_y)
                p_predict.append(tmp_p)
            filter.p = p_predict
             
            filter.weights = []
            for i in range(filter.N):
                w = filter.p[i].measurement_prob(Z, gtsm)
                filter.weights.append(w)
 
            w_sum = sum(filter.weights)
            for i in range(filter.N):
                filter.weights[i] /= w_sum
                s_s.append(filter.weights[i]*100+0.001)
            plt.scatter(p_x_s, p_y_s, c='r', s=s_s, alpha=0.8)


            filter.resample()

            print(eval_particals(real_car, filter.p))
            
            plt.pause(0.01)
    plt.ioff()
        

    
    
if __name__=="__main__":
    pass
    main()








