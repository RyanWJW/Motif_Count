import networkx as nx
import copy
import numpy as np
import pandas as pd
import math
import os
import time

#### 计算四节点网络模体度 ####

#### 第一种模体 ####
def cal_motif4_1(network):
    M4_1 = []
    for i in network:  # 遍历网络中所有节点
        j=network.out_degree(i)
        if j > 2:  # 取所有出度大于2的节点
            M4_1.append((j - 2) * (j - 1) * j / 6)
    return int(np.sum(M4_1))  # 列表中的数值的和即为第一种模体在网络中的数量


#### 第二种模体 ####
def cal_motif4_2(network):
    M4_2 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 0:  # 取所有出度大于0的节点
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                k=network.out_degree(j)
                if k > 1:  # 取所有出度大于1的子代节点
                    M4_2.append((k - 1) * k / 2)  # 将计算得到的结果添加到列表中
    return int(np.sum(M4_2))  # 列表中的数值的和即为第二种模体在网络中的数量


#### 第三种模体 ####
def cal_motif4_3(network):
    M4_3_1 = []
    M4_3_2 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 1:  # 取所有出度大于1的节点
            ss=network.out_degree(i)
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                if network.out_degree(j) > 0:  # 取所有出度大于0的子代节点
                    M4_3_1.append(ss)  # 将符合条件的节点出度的值添加到列表1中
                    M4_3_2.append(network.out_degree(j))  # 将符合条件的节点出度的值添加到列表2中
    M4_3_3 = (np.array(M4_3_1)-1) * np.array(M4_3_2) #- np.array(M4_3_2)  # 将计算的结果添加到列表3
    return sum(M4_3_3)  # 列表3的和即为第三种模体在网络中的数量


#### 第四种模体 ####
def cal_motif4_4(network):
    M4_4 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 0:  # 取所有出度大于0的节点
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                if network.out_degree(j) > 0:  # 取所有出度大于0的子节点
                    for k in network.successors(j):  # 遍历符合条件的节点的二代子节点
                        if network.out_degree(k) > 0:  # 取所有出度大于0的二代子节点
                            M4_4.append(network.out_degree(k))  # 将符合条件的节点出度的值添加到列表中
    return int(sum(M4_4))

#### 计算五节点网络模体度 ####


#### 第一种模体 ####
def cal_motif5_1(network):
    M5_1 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 0:  # 取所有出度大于0的节点
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                if network.out_degree(j) > 0:  # 取所有出度大于0的子节点
                    for k in network.successors(j):  # 遍历符合条件的节点的二代子节点
                        if network.out_degree(k) > 0:  # 取所有出度大于0的子节点
                            for l in network.successors(k):  # 遍历符合条件的节点的三代子节点
                                if network.out_degree(l) > 0:  # 取所有出度大于0的三代子节点
                                    M5_1.append(network.out_degree(l))  # 将符合条件的节点出度的值添加到列表中

    return int(sum(M5_1))


def cal_motif5_1_1(network):
    M5_1 = 0
    length= dict(nx.all_pairs_shortest_path_length(network))
    for i in length.values():
        a=np.array(list(i.values()))
        M5_1 += np.sum(a == 4)
    return M5_1

#### 第二种模体 ####
def cal_motif5_2(network):
    M5_2 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 0:  # 取所有出度大于0的节点
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                if network.out_degree(j) > 0:  # 取所有出度大于0的节点
                    for s in network.successors(j):  # 遍历符合条件的节点的子代节点
                        k = network.out_degree(s)
                        if k > 1:  # 取所有出度大于1的子代节点
                            M5_2.append((k - 1) * k / 2)  # 将计算得到的结果添加到列表中
    return int(np.sum(M5_2))  # 列表中的数值的和即为模体在网络中的数量


#### 第三种模体 ####
def cal_motif5_3(network):
    M5_3 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 0:  # 取所有出度大于0的节点
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                k = network.out_degree(j)
                if k > 2:  # 取所有出度大于2的节点
                    M5_3.append((k - 2) * (k - 1) * k / 6)
    return int(np.sum(M5_3))  # 列表中的数值的和即为模体在网络中的数量


#### 第四种模体 ####
def cal_motif5_4(network):
    M5_4_1 = []
    M5_4_2 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 0:  # 取所有出度大于0的节点
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                if network.out_degree(j) > 1:  # 取所有出度大于1的节点
                    ss = network.out_degree(j)
                    for k in network.successors(j):  # 遍历符合条件的节点的子代节点
                        if network.out_degree(k) > 0:  # 取所有出度大于0的子代节点
                            M5_4_1.append(ss)  # 将符合条件的节点出度的值添加到列表1中
                            M5_4_2.append(network.out_degree(k))  # 将符合条件的节点出度的值添加到列表2中
    M5_4_3 = (np.array(M5_4_1) - 1) * np.array(M5_4_2)  # - np.array(M4_3_2)  # 将计算的结果添加到列表3
    return sum(M5_4_3)  # 列表3的和即为模体在网络中的数量


#### 第五种模体 ####
def cal_motif5_5(network):
    M5_5_1 = []
    M5_5_2 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 1:  # 取所有出度大于1的节点
            ss = network.out_degree(i)
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                if network.out_degree(j) > 0:  # 取所有出度大于1的节点
                    for k in network.successors(j):  # 遍历符合条件的节点的子代节点
                        if network.out_degree(k) > 0:  # 取所有出度大于0的子代节点
                            M5_5_1.append(ss)  # 将符合条件的节点出度的值添加到列表1中
                            M5_5_2.append(network.out_degree(k))  # 将符合条件的节点出度的值添加到列表2中
    M5_5_3 = (np.array(M5_5_1) - 1) * np.array(M5_5_2)  # - np.array(M4_3_2)  # 将计算的结果添加到列表3
    return sum(M5_5_3)  # 列表3的和即为第三种模体在网络中的数量

def cal_motif5_5_1(network):
    M5_5_1 = []
    M5_5_2 = []

    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 1:  # 取所有出度大于0的节点
            ss = network.out_degree(i)
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                if network.out_degree(j) > 0:  # 取所有出度大于1的节点
                    M5_5_1.append(ss)  # 将符合条件的节点出度的值添加到列表1中
                    Ms = []
                    for k in network.successors(j):  # 遍历符合条件的节点的子代节点
                        if network.out_degree(k) > 0:  # 取所有出度大于0的子代节点
                            Ms.append(network.out_degree(k))  # 将符合条件的节点出度的值添加到列表1中
                    M5_5_2.append(sum(Ms))  # 将符合条件的节点出度的值添加到列表1中
    M5_5_3 = (np.array(M5_5_1) - 1) * np.array(M5_5_2)  # - np.array(M4_3_2)  # 将计算的结果添加到列表3
    return sum(M5_5_3)  # 列表3的和即为模体在网络中的数量

#### 第六种模体 ####
def cal_motif5_6(network):
    M5_6_1 = []
    M5_6_2 = 0
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 1:  # 取所有出度大于1的节点
            Ms = []
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                k = network.out_degree(j)
                if k > 0:  # 取所有出度大于0的子代节点
                    Ms.append(k)
            if Ms != []:
                Mas =np.array(Ms)
                ans=np.sum(np.dot(Mas[:,None],Mas[None,:]))-np.sum(Mas**2)
                M5_6_1.append(ans)  # 将计算得到的结果添加到列表中
    M5_6_2=sum(M5_6_1)/2# 列表中的数值的和即为模体在网络中的数量
    return int(M5_6_2)

#### 第七种模体 ####
def cal_motif5_7(network):
    M5_7_1 = []
    M5_7_2 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 1:  # 取所有出度大于1的节点
            ss = network.out_degree(i)
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                k = network.out_degree(j)
                if k > 1:  # 取所有出度大于1的子代节点
                    M5_7_2.append((k - 1) * k / 2)  # 将计算得到的结果添加到列表2中
                    M5_7_1.append(ss)
    M5_7_3 = (np.array(M5_7_1) - 1) * np.array(M5_7_2)
    return int(np.sum(M5_7_3))  # 列表3中的数值的和即为模体在网络中的数量

#### 第八种模体 ####
def cal_motif5_8(network):
    M5_7_1 = []
    M5_7_2 = []
    for i in network:  # 遍历网络中所有节点
        if network.out_degree(i) > 2:  # 取所有出度大于2的节点
            ss = network.out_degree(i)
            for j in network.successors(i):  # 遍历符合条件的节点的子代节点
                k = network.out_degree(j)
                if k > 0:  # 取所有出度大于1的子代节点
                    M5_7_2.append(k)  # 将计算得到的结果添加到列表2中
                    M5_7_1.append(ss)
    M5_7_3 = (np.array(M5_7_1) - 1) * (np.array(M5_7_1) - 2) * np.array(M5_7_2) / 2
    return int(np.sum(M5_7_3))  # 列表3中的数值的和即为模体在网络中的数量

#### 第九种模体 ####
def cal_motif5_9(network):
    M5_9 = []
    for i in network:  # 遍历网络中所有节点
        j = network.out_degree(i)
        if j > 3:  # 取所有出度大于3的节点
            M5_9.append((j - 3) * (j - 2) * (j - 1) * j / 24)
    return int(np.sum(M5_9))  # 列表中的数值的和即为模体在网络中的数量


if __name__ == "__main__":

    #原始网络
    # G0 = nx.read_edgelist("data/test2.txt", create_using=nx.DiGraph())
    data = pd.read_csv("data/politifact279.txt", sep=" ", names=["a", "b", "w"])
    # print(data.head())
    G0 = nx.from_pandas_edgelist(data, source="a", target="b", create_using=nx.DiGraph())
    t1=time.time()
    print(cal_motif5_1(G0))
    t2=time.time()
    print(t2-t1)



    # M = nx.number_of_edges(G0)
    #
    # a = cal_motif4_1(G0)
    #
    # b = cal_motif4_2(G0)
    # c = cal_motif4_3(G0)
    # d = cal_motif4_4(G0)


    # e = a + b + c + d
    # print('percent' , '\t' , 'count' , '\n'
    #     ' {:.8%}'.format(a/e) , '\t' , a , '\n'
    #     ' {:.8%}'.format(b/e) , '\t' , b , '\n'
    #     ' {:.8%}'.format(c/e) , '\t' , c , '\n'
    #     ' {:.8%}'.format(d/e) , '\t' , d , '\n')
