#-*-coding:UTF-8
'''
Created on 2018年9月6日
@author: mipapapa
车辆运动模型与感知模型
运动模式：转弯->前进
感知模式：获取语义分割结果的特征直方图
'''
import numpy as np
from math import *
from feature import Feature
from dataset import load_feature_npy
import random


class Vehile:
    """ 车辆的位置由TSM对应的边，以及在这条边上的1D行驶里程表示
    """
    def __init__(self, edges_num=10):
        self.edge_id = int(random.random() * edges_num)
        self.odometry = 0
        self.forward_noise = 0.0
        self.k = 1.0    # 角度误差增益
    
    def __repr__(self):
        return 'ei=%d odo=%.3f' % (self.edge_id, self.odometry)
    
    def set(self, new_edge_id, new_odo):
        self.edge_id = new_edge_id
        self.odometry = new_odo
        
    def set_noise(self, new_f_noise):
        self.forward_noise = float(new_f_noise)
    
    def loc(self, gtsm):
        """ 根据gtsm以及车辆当前的边以及里程，转换为车的位置
        """
        self.x = 0
        self.y = 0
        self.theta = 0
    
    def gaussian(self, mu, sigma, x):
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    def sense(self, ft):
        """ 读取真实世界中当前观测的语义信息
            现使用数据集在中数据代替
        """
        self.rec_feature = ft
        return ft
        
    def move(self, forward_distance, gtsm):
        """ 车辆状态转移关系
        forward_distance: 车辆前进的距离
        gtsm: 已知地图
        """
        self.forward_noise = forward_distance*forward_distance
        distance = random.gauss(forward_distance, self.forward_noise)
        self.odometry += distance
        # 获取当前车辆对应的边缘
        cur_edge = gtsm.edges[self.edge_id]
        
        if 0 <= self.odometry <= cur_edge.d:
            # 当新的里程累计数位于边的内部， 维持当前车辆的边
            self.edge_id = self.edge_id
            
        elif self.odometry > cur_edge.d:
            # 当新的里程超越对应边时， 从当前边终点的节点中，随机选择一条出边
            tmp_len = gtsm.edges[self.edge_id].d
            while self.odometry > tmp_len:
                ending_node = gtsm.nodes[gtsm.edges[self.edge_id].ending_node_id]
                self.edge_id = int(random.random()*len(ending_node.edges_from_this))
                self.odometry -= tmp_len
                tmp_len = gtsm.edges[self.edge_id].d
        else:
            # 当新的里程落后对应边时， 从当前边起点的节点中，随机选择一条入边
            tmp_len = gtsm.edges[self.edge_id].d
            while self.odometry < 0:
                starting_node = gtsm.nodes[gtsm.edges[self.edge_id].starting_node_id]
                self.edge_id = int(random.random()*len(starting_node.edges_to_this))
                self.odometry += tmp_len
                tmp_len = gtsm.edges[self.edge_id].d
            self.odometry = tmp_len - self.odometry     # 转换为以对应边起点的里程数
        
    def measurement_prob(self, measurement, gtsm):
        # 观测似然，描述当前车辆所记载的观测值与
        cur_edge_feat = gtsm.edges[self.edge_id]
        d = measurement - cur_edge_feat
        dtheta = self.k * np.cos(measurement % cur_edge_feat)
        prob = np.exp(d) * np.exp(dtheta)
        return prob
    
            
def main():
    feature_lst = load_feature_npy(r"dataset/ts_seq1_feature.npy")
    # 将数据转换为车辆的控制
    
    myrobot = Vehile()
    
    for t in range(len(feature_lst)):
        Ft = feature_lst[t]
        Z = myrobot.sense(Ft)
        
        
        
    
if __name__=="__main__":
    pass
    main()

