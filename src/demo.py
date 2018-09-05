#-*-coding:UTF-8
'''
Created on 2018年9月5日
@author: mipapapa
'''


import networkx as nx 
import matplotlib.pyplot as plt 

colors = ['red', 'green', 'blue', 'yellow'] 
#有向图 
DG = nx.DiGraph() 
#一次性添加多节点，输入的格式为列表 
DG.add_nodes_from(['A', 'B', 'C', 'D']) 
#添加边，数据格式为列表 
DG.add_edges_from([('A', 'B'), ('A', 'C'), ('A', 'D'), ('D','A')]) 
#作图，设置节点名显示,节点大小，节点颜色 
nx.draw(DG,with_labels=True, node_size=900, node_color = colors) 
plt.show() 

def main():
    pass
    
if __name__=="__main__":
    pass
    main()

