#-*-coding:UTF-8
'''
Created on 2018年9月6日
@author: mipapapa

TSM显示模块
1 描画边和节点
2 
'''
import matplotlib.pyplot as plt


def plotTSM(tsm):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    print("num nodes: %d" % (len(tsm.nodes)))
    print("num edges: %d" % (len(tsm.edges)))
    for i in range(len(tsm.nodes)):
        node = tsm.nodes[i]
        plt.scatter(node.x, node.y, s=40, alpha=1.0)
    
    for i in range(len(tsm.edges)):
        edge = tsm.edges[i]
        if edge.starting_node_id == -1 or edge.ending_node_id == -1:
            continue
        n0 = tsm.nodes[edge.starting_node_id]
        n1 = tsm.nodes[edge.ending_node_id]
        ax.arrow(n0.x, n0.y, n1.x-n0.x, n1.y-n0.y, 
                 head_width=0.8, head_length=0.8, 
                 fc='b', ec='r', alpha=0.9)
    
    plt.show()



    
    