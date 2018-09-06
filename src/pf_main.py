#-*-coding:UTF-8-*-
'''
Created on 2018年9月6日
@author: mipapapa

粒子滤波器实现

# 从P中抽取概率与对应的W值成正比的粒子
# 该代码可以重复应用的任何粒子滤波器上
'''

from math import *
import random
from partical_filter.robot import *

def main():
    ####   DON'T MODIFY ANYTHING ABOVE HERE! ENTER/MODIFY CODE BELOW ####
    myrobot = robot()
    myrobot = myrobot.move(0.1, 5.0)
    Z = myrobot.sense()
    N = 1000
    T = 10 #Leave this as 10 for grading purposes.
    
    p = []
    for i in range(N):
        r = robot()
        r.set_noise(0.05, 0.05, 5.0)
        p.append(r)
    
    for t in range(T):
        myrobot = myrobot.move(0.1, 5.0)
        Z = myrobot.sense()
    
        p2 = []
        for i in range(N):
            p2.append(p[i].move(0.1, 5.0))
        p = p2
    
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(Z))
    
        p3 = []
        index = int(random.random() * N)
        beta = 0.0
        mw = max(w)
        for i in range(N):
            beta += random.random() * 2.0 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        p = p3
        #enter code here, make sure that you output 10 print statements.
        
        print eval(myrobot, p)
    

    
if __name__=="__main__":
    pass
    main()