#coding:UTF-8
'''
Created on 2018年9月2日-下午5:41:45
author: Gary-W
基于feature构建的拓扑地图模块
'''
import numpy as np
from feature import Feature, N_SEMATIC_CLASS

class Edge:
    """ Edge用于表示一段道路的区域
    在TSM中，Edge表示一段具有相似的方向与语义直方图的连续观测图像组成的区域
    """
    def __init__(self):
        self.id = 0         # the edge id
        self.length = 0     # len of the edge
        self.theta = 0      # mean orientation of the edge
        self.h_l = np.zeros((N_SEMATIC_CLASS))  # 左侧语义直方图
        self.h_c = np.zeros((N_SEMATIC_CLASS))  # 中侧语义直方图
        self.h_r = np.zeros((N_SEMATIC_CLASS))  # 右侧语义直方图
        self.start_node_id = None
        self.end_node_id = None

class Node:
    """ Node用于表示两条Edge之间的相交和连接
    """
    def __init__(self):
        self.edges_start = []   # 所有以该节点为起点的边
        self.edges_end = []     # 所有以该节点为终点的边


class TSM:
    def __init__(self):

        self.FEAT_DIST_THS = 100    # 特征差异阈值
        self.MAX_SIM_ACC_CNT = 5    # 最大相似特征合并次数
        self._tmp_sim_acc_cnt = 0
        
    def observation(self, feat_cur):
        """ 通过输入图像的特征进行观察，进行特征序列的更新
            若存在相似特征，进行合并
        """
        d = feat_cur - self.F_SO_last
        if self._tmp_sim_acc_cnt < self.MAX_SIM_ACC_CNT and d < self.FEAT_DIST_THS:
            self.F_SO_last = self.F_SO_last + feat_cur
            self._tmp_sim_acc_cnt += 1
        else:
            self.F_SO_last = feat_cur
            self._tmp_sim_acc_cnt = 1

    def mapping(self):
        pass



def main():
    from dataset import load_feature_npy

    tsm = TSM()
    load_feature_npy(r"dataset/ts_seq1_feature.npy")



if __name__=="__main__":
    pass
    main()








