#coding:UTF-8
'''
Created on 2018年9月2日-下午6:27:42
author: Gary-W
基于字典的图结构
'''
class Vertex(object):
    def __init__(self, label=''):
        self.label = label
    
    def __repr__(self):
        return "V(%s)" % (repr(self.label))

class Edge(tuple):
    def __new__(cls, e1, e2):
        return tuple.__new__(cls, e1, e2)

    def __repr__(self):
        return "E(%s, %s)" % (repr())
    
class Graph(dict):
    def __init__(self, vs=[], es=[]):
        """ 构建一个新图:
        vs: 节点列表， es: 边列表
        """
        for v in vs:
            self.add_vertex(v)
        
        for e in es:
            self.add_edge(e)
    
    def add_vertex(self, v):
        """ 在图中加入一个节点，使用节点的hashcode作为字典索引
        """
        self[v] = {}
    
    def add_edge(self, e):
        """ 在图中加入一条边，如果存在的节点间已有边，使用新边替代
        """
        v, w = e
        self[v][w] = e
        self[w][v] = e
        
if __name__=="__main__":
    pass

