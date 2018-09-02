#coding:UTF-8
'''
Created on 2018年9月2日-下午5:41:45
author: Gary-W
基于feature构建的拓扑地图模块
'''
from data.feature import Feature

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
            

if __name__=="__main__":
    pass

