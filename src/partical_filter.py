#-*-coding:UTF-8
'''
Created on 2018年9月6日
@author: mipapapa
基于粒子滤波的定位模块
'''

import random

class ParticalFilter:
    """ 粒子滤波模块
    """
    def __init__(self, n_particals=1000):
        self.N = n_particals
        self.p = []
        self.weights = []
        
    def create_particals(self, product_factory):
        """ 创建 N 个粒子, 使用product_factory返回的对象作为粒子的个体
        """
        for _i in range(self.N):
            new_obj = product_factory()
            self.p.append(new_obj)
    
    def update_particals(self, update_func):
        p_predict = []
        for i in range(self.N):
            update_func(self.p[i])
            p_predict.append(self.p[i])
        self.p = p_predict
    
    
    def update_weights(self, weight_func, measurement):
        self.weights = []
        for i in range(self.N):
            w = weight_func(self.p[i], measurement)
            self.weights.append(w)
    
    def resample(self):
        """ 使用轮盘更新法进行粒子重采样
        """
        p_resample = []
        index = int(random.random() * self.N)
        beta = 0.0
        mw = max(self.weights)
        for i in range(self.N):
            beta += random.random() * 2.0 * mw
            while beta > self.weights[index]:
                beta -= self.weights[index]
                index = (index + 1) % self.N
            p_resample.append(self.p[index])
        self.p = p_resample
        
        

def main():
    pass
    
if __name__=="__main__":
    pass
    main()

