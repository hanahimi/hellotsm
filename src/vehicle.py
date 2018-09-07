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
        self.k = 1.0            # 角度误差增益(平衡参数)
    
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
        ns_id = gtsm.edges[self.edge_id].starting_node_id
        self.x = gtsm.nodes[ns_id].x
        self.y = gtsm.nodes[ns_id].y
        self.theta = gtsm.edges[self.edge_id].theta

        self.x += self.odometry * np.sin(self.theta)
        self.y += self.odometry * np.cos(self.theta)

        return self.x, self.y, self.theta
    
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
#         self.forward_noise = forward_distance*forward_distance
        distance = random.gauss(forward_distance, self.forward_noise)
        self.odometry += distance
        cur_edge = gtsm.edges[self.edge_id]
        
        if 0 <= self.odometry <= cur_edge.d:    
            # 当新的里程累计数位于边的内部， 维持当前车辆的边
            self.edge_id = self.edge_id
            
        elif self.odometry > cur_edge.d:
            # 当新的里程超越对应边时， 从当前边终点的节点中，随机选择一条出边
            tmp_len = gtsm.edges[self.edge_id].d
            while self.odometry > tmp_len:
                ending_node = gtsm.nodes[gtsm.edges[self.edge_id].ending_node_id]
                self.edge_id = random.choice(ending_node.edges_from_this)
                self.odometry -= tmp_len
                tmp_len = gtsm.edges[self.edge_id].d
            
        else:   
            # 当新的里程落后对应边时， 从当前边起点的节点中，随机选择一条入边
            tmp_len = gtsm.edges[self.edge_id].d
            while self.odometry < 0:
                starting_node = gtsm.nodes[gtsm.edges[self.edge_id].starting_node_id]
                self.edge_id = random.choice(starting_node.edges_to_this)
                self.odometry += tmp_len
                tmp_len = gtsm.edges[self.edge_id].d
            self.odometry = tmp_len - self.odometry     # 转换为以对应边起点的里程数
        
        # move操作 必须返回实体，否则粒子更新时全部对于同一对象
        res = Vehile()
        res.set(self.edge_id, self.odometry)
        res.set_noise(self.forward_noise)
        return res
        
    def measurement_prob(self, measurement, gtsm):
        # 观测似然，描述当前车辆所记载的观测值与GTSM中对应边特征的差异即 P(Z|X)
        cur_edge_feat = gtsm.edges[self.edge_id]
        d = measurement - cur_edge_feat
        self.k = 10
        t1 = measurement.theta
        t2 = cur_edge_feat.theta

#         print("M:%2.2f  P:%2.2f" % (np.rad2deg(t1), np.rad2deg(t2)))
        
        r = np.cos(t1)*np.cos(t2) + np.sin(t1)*np.sin(t2)
#         print(np.rad2deg(r))
        dtheta = self.k * r
#         print(dtheta, np.rad2deg(measurement.theta), np.rad2deg(cur_edge_feat.theta))
        # TODO:误差需要与里程值相关
#         prob = np.exp(-d) * np.exp(dtheta)
        prob = np.exp(-d)
#         prob = np.exp(dtheta)
        
        return prob
    

def eval_particals(veh_real, partical):
    """ 评估粒子群定位位置对于真实车辆定位位置的命中率
    """
    _sum = 0.0
    real_edge = veh_real.edge_id
#     real_odo = robot.odometry
    
    for i in range(len(partical)): # calculate mean error
        _edge_id = partical[i].edge_id
        if _edge_id == real_edge:
            _sum += 1
            
    return _sum / float(len(partical))

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

