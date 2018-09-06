#coding:UTF-8
'''
Created on 2018年9月2日-下午5:41:45
author: Gary-W
基于feature构建的拓扑地图模块
'''
from feature import Feature
import random

class SemaObservation:
    """ 计算融合语义观测向量 F_SO
    """
    def __init__(self):
        self.fso = None
        self.n = 0
        self.Nf = 5    # 最大相似特征累计次数
        self.FEAT_DIST_THS = 0.05    # 特征差异阈值
    
    def new_semanitic_observation(self, img_pose_feat):
        Ft = Feature()
        Ft.copy(img_pose_feat)
        return Ft
    
    def input(self, img_pose_feat):
        """ 输入图像/位置特征 F(t), 尝试与F_SO(t-1) 进行融合
        """
        if not self.fso:
            self.fso = img_pose_feat
            self.n = 1
        else:
            d = self.fso - img_pose_feat
            if d < self.FEAT_DIST_THS and self.n < self.Nf:
                self.fso = self.fso + img_pose_feat
                self.n += 1
            else:
                self.fso = self.new_semanitic_observation(img_pose_feat)
                self.n = 1

        return self.fso

class Edge(Feature):
    """ Edge用于表示一段道路的区域
        在TSM中，Edge表示一段具有相似的方向与语义直方图的连续观测图像组成的区域
        Edge 继承 Feature 结构，对其中属性重新定义如下：
            d: 边的长度，表示一段区域的路径范围
            theta: 该路段的平均航向角度
    """
    def __init__(self, _id=0):
        Feature.__init__(self)
        self.id = _id         # Edge_ID（用于显示）
        self.feature = Feature()
        
        self.starting_node_id = -1
        self.ending_node_id = -1
    
    def __repr__(self):
        return "E_id:%d, sn:%d, en:%d" % (self.id, self.starting_node_id, self.ending_node_id)

class Node:
    """ Node用于表示两条Edge之间的相交和连接（可以认为是路的节点）
    """
    def __init__(self, _id=0):
        self.id = _id             # Node_ID（用于显示）
        self.edges_from_this = []   # 所有以该节点为起点的边(id)(出边)
        self.edges_to_this = []     # 所有以该节点为终点的边(id)(入边)
        self.x = 0
        self.y = 0
        
    def __repr__(self):
        return "N_id:%d, es:%s, ee:%s" % (self.id, 
                                          str(self.edges_from_this), 
                                          str(self.edges_to_this))
            
class TSM:
    """ Topological Semantic Mapping
    """
    def __init__(self):
        self.edges = []
        self.nodes = []
    
        self.MAPPING_THS = 0.02     # 特征距离匹配阈值
        self.ORIENT_DIFF_THS = 5    # 角度变化阈值(deg)
        
    def show_TSM(self):
        print("tms data")
        for i in range(len(self.nodes)):
            print(self.nodes[i])
        for i in range(len(self.edges)):
            print(self.edges[i])
    
    def __new_node(self):
        n_nodes = len(self.nodes)
        tmp_node = Node(_id = n_nodes)
        self.nodes.append(tmp_node)
        return self.nodes[-1]
    
    def __new_edge(self, fso=None):
        n_edges = len(self.edges)
        tmp_edge = Edge(_id = n_edges)
        if fso:
            tmp_edge.copy(fso)
        
        self.edges.append(tmp_edge)
        return self.edges[-1]
    
    def __connect_nen(self, start_node, in_edge, end_node=None):
        """ 关联两个节点以及中间的一条边
            start_node： 起始节点 A
            end_node: 中间节点 B
            in_edge: 边（A->B）
        """
        in_edge.starting_node_id = start_node.id
        start_node.edges_from_this.append(in_edge.id)
        if end_node:
            in_edge.ending_node_id = end_node.id
            end_node.edges_to_this.append(in_edge.id)
    
    def __connect_ene(self, in_edge, node, out_edge=None):
        """ 关联两个边以及中间的一个节点
            in_edge： 进入节点n的边 A
            in_node: 中间节点 A->n->B
            out_edge: 退出节点n的边 B
        """
        in_edge.ending_node_id = node.id
        node.edges_to_this.append(in_edge.id)
        if out_edge:
            out_edge.starting_node_id = node.id
            node.edges_from_this.append(out_edge.id)
    
    
    def mapping(self, fso):
        """ 根据新的特征观测，对TSM进行更新
        """
        if not self.edges and not self.nodes:
            new_node = self.__new_node()
            m_last = self.__new_edge(fso)
            self.__connect_nen(new_node, m_last)

            new_node.x = fso.x
            new_node.y = fso.y
            
        else:
            m_last = self.edges[-1]
            dhist = m_last - fso
            dtheta = m_last % fso
             
            if dhist < self.MAPPING_THS and dtheta < self.ORIENT_DIFF_THS:
                m_last_tmp = m_last + fso
                m_last.copy(m_last_tmp)
 
            else:
                new_node = self.__new_node()
                new_node.x = fso.x
                new_node.y = fso.y
                
                self.__connect_ene(m_last, new_node)
                m_last = self.__new_edge(fso)
                self.__connect_nen(new_node, m_last)
    
    def close_looping(self):
        """ 手动close_looping, 需要车辆回到出发起点
        """
        node_start = self.nodes[0]
        m_last = self.edges[-1]
        edge_end = self.nodes[-1]
        self.__connect_nen(edge_end, m_last, node_start)
    
    
    def random_edge(self):
        """ 根据以建好后的TSM，随机返回一个边的id
        """
        rand_edge_id = int(random.random() * len(self.edges))
        return rand_edge_id
        
def main():
    from dataset import load_feature_npy
    from display import plotTSM
    
    feature_lst = load_feature_npy(r"dataset/ts_seq1_feature.npy")

    tsm = TSM()
    sov = SemaObservation()
    for t in range(len(feature_lst)):
        Ft = feature_lst[t]
        fso = sov.input(Ft)
        tsm.mapping(fso)
    tsm.close_looping()
    
    plotTSM(tsm)

    
    
if __name__=="__main__":
    pass
    main()








