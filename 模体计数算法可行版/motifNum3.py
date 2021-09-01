import networkx as nx
import time
from collections import deque

def Feasibility_weighted(G,G_motif,n1,n2,N1,node,hasEdge):
    """
    根据同构条件判断是否是要寻找的模体
    :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
    :param G_motif: 模体图,可以有向或者无向但必须与图G一致
    :param n1: 模体网络G_motif中的节点
    :param n2: 模体网络G_motif中的节点
    :param N1: 目标网络G中的节点
    :param node: 目标网络G中的节点
    :param hasEdge: n1和n2之间是否有正向边
    :return True or False: 代表是否构成模体
    """
    if hasEdge:
        if(G_motif[n1][n2]['weight'])!= (G[N1][node]['weight']):
            return False

    return True

def Feasibility_weighted_directed(G,G_motif,n1,n2,N1,node,hasEdge,hasEdge1):
    """
    根据同构条件判断是否是要寻找的模体
    :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
    :param G_motif: 模体图,可以有向或者无向但必须与图G一致
    :param n1: 模体网络G_motif中的节点
    :param n2: 模体网络G_motif中的节点
    :param N1: 目标网络G中的节点
    :param node: 目标网络G中的节点
    :param hasEdge: n1和n2之间是否有正向边
    :param hasEdge1: n2和n1之间是否有反向边
    :return True or False: 代表是否构成模体
    """
    if hasEdge1:
        if (G_motif[n2][n1]['weight'])!= (G[node][N1]['weight']):
            return False

    if hasEdge:
        if (G_motif[n1][n2]['weight'])!= (G[N1][node]['weight']):
            return False

    return True

def preSort(G_motif,G2_node_list):
    """
    预处理：排序，调整搜索顺序，将度大的放前面，这样约束越多，剪枝越多，搜索越快。
    :param G_motif:
    :param G2_node_list:
    :param n_G2:
    """
    n_G2=len(G2_node_list)
    for i in range(1,n_G2):
        for j in range(0,n_G2-i):
            if G_motif.degree(G2_node_list[j+1])>G_motif.degree(G2_node_list[j]):
                t=G2_node_list[j]
                G2_node_list[j]=G2_node_list[j+1]
                G2_node_list[j+1]=t

def vf2_motif(G,G_motif,G_node_list,G2_node_list,n_G2,MS,deeps,weighted=False):
    # start = time.time()

    number = 0  # 存储模体数量
    deep = deeps
    SL=[]
    for i in range(n_G2-deeps):
        SL.append([])
        for j in range(0,n_G2-deeps-i):
            SL[i].append([])
    for j in range(deeps, n_G2):
        searchset = set(G_node_list)
        searchset = searchset - set(MS[0:deeps])
        ss=[]
        for i in range(deeps):
            hasEdge=G_motif.has_edge(G2_node_list[i], G2_node_list[j])
            if (hasEdge):
                searchset = searchset & set(G.neighbors(MS[i]))
            else:
                searchset = searchset - set(G.neighbors(MS[i]))
            if (not searchset):
                return 0

            if weighted:
                for k in searchset:
                    if (not Feasibility_weighted(G, G_motif, G2_node_list[i], G2_node_list[j], MS[i], k,hasEdge)):
                        ss.append(k)
            searchset=searchset-set(ss)
        if (not searchset):
            return 0
        SL[0][j-deeps]=  searchset
    if n_G2 - deeps < 2:
        return len(SL[0][0])
    Quelist = []
    for i in range(n_G2 - deeps - 1):
        Quelist.append(deque())

    Quelist[deep - deeps].extend(SL[deep - deeps][0])
    ddd = False
    while (1):
        if  deep == n_G2 - 1:
            number += len(SL[deep-deeps][0])
            deep -= 1
        while (not Quelist[deep - deeps]):
            deep -= 1
            if deep < deeps:
                return number
        MS[deep] = Quelist[deep - deeps].pop()
        for i in range(1,n_G2-deep):
            searchset = SL[deep-deeps][i]
            searchset = searchset - set(MS[0:deep+1])
            hasEdge= G_motif.has_edge(G2_node_list[deep], G2_node_list[deep+i])
            if (hasEdge):
                searchset = searchset & set(G.neighbors(MS[deep]))
            else:
                searchset = searchset - set(G.neighbors(MS[deep]))

            if (not searchset):
                ddd = False
                break
            ss=[]

            if weighted:
                for k in searchset:
                    if (not Feasibility_weighted(G, G_motif, G2_node_list[deep], G2_node_list[deep+i], MS[deep], k,hasEdge)):
                        ss.append(k)
            searchset=searchset-set(ss)
            if (not searchset):
                ddd = False
                break
            else:
                SL[deep - deeps+1][i-1] = searchset
                ddd = True
        if ddd:
            deep += 1
            if deep < n_G2-1:
                Quelist[deep - deeps].extend(SL[deep-deeps][0])

def vf2_motif_directed(G,G_motif,G_node_list,G2_node_list,n_G2,MS,deeps,weighted=False):
    # start = time.time()
    # print("@@@@@",G2_node_list)
    edgelist = list(nx.edges(G))
    edgelist1 = []
    for i in edgelist:
        edgelist1.append((i[1], i[0]))
    G2 = nx.from_edgelist(edgelist1, create_using=nx.DiGraph())

    number = 0  # 存储模体数量
    deep = deeps
    SL=[]
    for i in range(n_G2-deeps):
        SL.append([])
        for j in range(0,n_G2-deeps-i):
            SL[i].append([])
    for j in range(deeps, n_G2):
        searchset = set(G_node_list)
        searchset = searchset - set(MS[0:deeps])
        ss=[]
        for i in range(deeps):
            hasEdge=G_motif.has_edge(G2_node_list[i], G2_node_list[j])
            hasEdge1 = G_motif.has_edge(G2_node_list[j], G2_node_list[i])
            if (hasEdge):
                searchset = searchset & set(G.neighbors(MS[i]))
            else:
                searchset = searchset - set(G.neighbors(MS[i]))
            if (hasEdge1):
                searchset = searchset & set(G2.neighbors(MS[i]))
            else:
                searchset = searchset - set(G2.neighbors(MS[i]))
            if (not searchset):
                return 0
            if weighted:
                for k in searchset:
                    if ( not Feasibility_weighted_directed(G, G_motif, G2_node_list[i], G2_node_list[j], MS[i], k,hasEdge,hasEdge1)):
                        ss.append(k)
            searchset=searchset-set(ss)
        if (not searchset):
            return 0
        SL[0][j-deeps]=  searchset
    if n_G2 - deeps < 2:
        return len(SL[0][0])
    Quelist = []
    for i in range(n_G2 - deeps - 1):
        Quelist.append(deque())

    Quelist[deep - deeps].extend(SL[deep - deeps][0])
    ddd = False
    # print(Quelist)
    while (1):
        if  deep == n_G2 - 1:
            number += len(SL[deep-deeps][0])
            deep -= 1
        while (not Quelist[deep - deeps]):
            deep -= 1
            if deep < deeps:
                return number
        MS[deep] = Quelist[deep - deeps].pop()
        for i in range(1,n_G2-deep):
            searchset = SL[deep-deeps][i]
            searchset = searchset - set(MS[0:deep+1])
            hasEdge= G_motif.has_edge(G2_node_list[deep], G2_node_list[deep+i])
            hasEdge1 = G_motif.has_edge(G2_node_list[deep+i], G2_node_list[deep])
            if (hasEdge):
                searchset = searchset & set(G.neighbors(MS[deep]))
            else:
                searchset = searchset - set(G.neighbors(MS[deep]))
            if (hasEdge1):
                searchset = searchset & set(G2.neighbors(MS[deep]))
            else:
                searchset = searchset - set(G2.neighbors(MS[deep]))

            if (not searchset):
                ddd = False
                break
            ss=[]
            if weighted:
                for k in searchset:
                    if ( not Feasibility_weighted_directed(G, G_motif, G2_node_list[deep], G2_node_list[deep+i], MS[deep], k,hasEdge,hasEdge1)):
                        ss.append(k)
            searchset=searchset-set(ss)
            if (not searchset):
                ddd = False
                break
            else:
                SL[deep - deeps+1][i-1] = searchset
                ddd = True
        if ddd:
            deep += 1
            if deep < n_G2-1:
                Quelist[deep - deeps].extend(SL[deep-deeps][0])



def node_motif_num(G,G_motif,node,directed=False,weighted=False):
    """
        计算node节点作为模体的第一个节点所参与的模体数量
        :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
        :param G_motif: 模体图,可以有向或者无向但必须与图G一致
        :param node: 图G中的一个节点
        :param directed: 是否是有向图，是有向图值为True，否则为False，默认为无向图False
        :param weighted: 是否具有权重，是否是加权网络，若是值为True，若否值为False，默认为False,符号网络视为加权网络。
        :return :点模体数
    """

    # start = time.time()
    G_node_list = list(nx.nodes(G))
    G2_node_list = list(nx.nodes(G_motif))
    len1 = len(G2_node_list)
    preSort(G_motif, G2_node_list[1:len1])  # 调整搜索顺序
    MS = ['*' for x in range(len1)]
    MS[0] = node
    node_motif_number = 0
    repetitions = 0
    if directed:
        # 下面查找node节点的模体数
        node_motif_number = vf2_motif_directed(G, G_motif, G_node_list, G2_node_list, len1, MS, 1,weighted)
        if node_motif_number==0:
            return 0
        #搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        repetitions = vf2_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 1,weighted)
    else:
        node_motif_number = vf2_motif(G, G_motif, G_node_list, G2_node_list, len1, MS, 1, weighted)
        if node_motif_number==0:
            return 0
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        repetitions = vf2_motif(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 1, weighted)
    # end = time.time()
    # print("node_motif_num总共用时{}秒".format((end - start)))
    #结果是需要除以重复的数
    return node_motif_number/repetitions

def edge_motif_num(G,G_motif,edge,directed=False,weighted=False):
    """
        计算node节点作为模体的第一个节点所参与的模体数量
        :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
        :param G_motif: 模体图,可以有向或者无向但必须与图G一致
        :param edge: 图G中的一条边
        :param twoWay: 是否为双向边或无向边，如果是twoWay的值是True，否则为False，默认为False
        :param directed: 是否是有向图，是有向图值为True，否则为False，默认为无向图False
        :param weighted: 是否具有权重，是否是加权网络，若是值为True，若否值为False，默认为False,符号网络视为加权网络。
        :return :返回值是边模体数
    """
    twoWay = False
    if not G.has_edge(edge[0],edge[1]):
        print("There is no such edge in the network.")
    if G.has_edge(edge[1],edge[0]):
        twoWay=True

    # start = time.time()
    G_node_list = list(nx.nodes(G))
    G2_node_list = list(nx.nodes(G_motif))
    len1 = len(G2_node_list)
    preSort(G_motif, G2_node_list[2:len1])  # 调整搜索顺序
    MS = ['*' for x in range(len1)]
    edge_motif_number=0
    repetitions =0
    if directed:
        # 计算边模体数量01的顺序不同
        MS[0] = edge[0]
        MS[1] = edge[1]
        edge_motif_number = vf2_motif_directed(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, weighted)

        if twoWay:  # 如果是双向边还需要查找反方向的模体数
            MS[0] = edge[1]
            MS[1] = edge[0]
            edge_motif_number += vf2_motif_directed(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, weighted)
        if edge_motif_number ==0:
            return 0
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        MS[1] = G2_node_list[1]
        repetitions = vf2_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, weighted)
        if twoWay:
            MS[0] = G2_node_list[1]
            MS[1] = G2_node_list[0]
            repetitions += vf2_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, weighted)
    else:
        MS[0] = edge[0]
        MS[1] = edge[1]
        edge_motif_number = vf2_motif(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, weighted)

        if twoWay:  # 如果是双向边还需要查找反方向的模体数
            MS[0] = edge[1]
            MS[1] = edge[0]
            edge_motif_number += vf2_motif(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, weighted)
        if edge_motif_number == 0:
            return 0
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        MS[1] = G2_node_list[1]
        repetitions = vf2_motif(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, weighted)
        if twoWay:
            MS[0] = G2_node_list[1]
            MS[1] = G2_node_list[0]
            repetitions += vf2_motif(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, weighted)
    # end = time.time()
    # print("edge_motif_num总共用时{}秒".format((end - start)))
    # 结果是需要除以重复的数
    return edge_motif_number/repetitions


def total_motif_num(G,G_motif,directed=False,weighted=False):
    """
        计算模体总数
        :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
        :param G_motif: 模体图,可以有向或者无向但必须与图G一致
        :param directed: 是否是有向图，是有向图值为True，否则为False，默认为无向图False
        :param weighted: 是否具有权重，是否是加权网络，若是值为True，若否值为False，默认为False,符号网络视为加权网络。
        :return :返回值是模体总数
    """
    G_node_list = list(nx.nodes(G))
    G2_node_list = list(nx.nodes(G_motif))
    n_G2 = len(G2_node_list)
    # start = time.time()

    preSort(G_motif, G2_node_list)  # 调整搜索顺序
    MS = ['*' for x in range(n_G2)]
    total_motif_number = 0
    repetitions = 0
    # 计算模体总数量
    if directed:
        total_motif_number = vf2_motif_directed(G, G_motif, G_node_list, G2_node_list, n_G2, MS, 0, weighted)
        if total_motif_number==0:
            return 0
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        repetitions = vf2_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0, weighted)

    else:
        total_motif_number = vf2_motif(G, G_motif, G_node_list, G2_node_list, n_G2, MS, 0,weighted)
        if total_motif_number==0:
            return 0
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        repetitions = vf2_motif(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0,weighted)
    # end = time.time()
    # print("total_motif_num总共用时{}秒".format((end - start)))
    # 结果是需要除以重复的数
    return total_motif_number / repetitions


if __name__ == "__main__":
    # G = nx.DiGraph()
    # l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # s = [(1, 2), (1, 3), (3, 4), (2, 4), (1, 4), (1, 5), (5, 8), (8, 2), (7, 8), (5, 2), (9, 6), (5, 9), (6, 8), (6, 7)]
    # G.add_nodes_from(l)
    # G.add_edges_from(s)
    # g = nx.DiGraph()
    # g.add_nodes_from([1, 2, 3])
    # g.add_edges_from([(1, 2), (2, 3), (1, 3)])
    # edge = (1, 2)
    # number = edge_motif_num(G, g, edge, twoWay=True)
    # number1 = node_motif_num(G, g, 2)
    # number2 = total_motif_num(G, g)
    # print('边摸体数量', number, number1, number2)

    # import pandas as pd
    # aa=pd.read_csv("mydata/netscience.csv")
    # G = nx.from_pandas_edgelist(aa,'src','dst',create_using=nx.DiGraph())
    # G = nx.read_edgelist("mydata/test.txt", create_using=nx.Graph())
    # G = nx.read_weighted_edgelist("mydata/new_bitcoinalpha.txt", create_using=nx.DiGraph())
    # G_motif = nx.read_weighted_edgelist("mydata/motif/motif4_1.txt", create_using=nx.DiGraph())
    # edgelist = list(nx.edges(G))
    # node_list=list(nx.nodes(G))
    # # print(edgelist)
    # # edge=edgelist[57]
    # number=0
    # number1=0
    # number2=0
    # # print(edge_motif_num(G, G_motif, edge, twoWay=True))
    # start1=time.time()
    # for edge in edgelist:
    #     number += edge_motif_num(G, G_motif, edge,twoWay=True,directed=True,weighted=True)
    # end1=time.time()
    # print('my motif ', number, 'time ', end1 - start1)
    # # start2=time.time()
    # # for edge in edgelist:
    # #     number1+= mf.m12(edge[0],edge[1],G)
    # # end2=time.time()
    #
    # # print('his motif ', number1, 'time ',end2 - start2)
    #
    # start3 = time.time()
    # print(total_motif_num(G, G_motif,directed=True,weighted=True))
    # end3 = time.time()
    # print('all motif ' 'time ', end3 - start3)
    #
    # start4 = time.time()
    # for edge in edgelist:
    #     number2 += node_motif_num(G, G_motif, edge[0],directed=True,weighted=True)
    # end4 = time.time()
    # print('node motif ', number2, 'time ', end4 - start4)
################################
    # edge = edgelist[5]
    # start1=time.time()
    # for i in range(100000):
    #     G.has_edge(edge[1],edge[0])
    # end1=time.time()
    # start2=time.time()
    # for i in range(100000):
    #     (edge[0],edge[1]) in edgelist or (edge[1],edge[0]) in edgelist
    # end2=time.time()
    # start3 = time.time()
    # for i in range(100000):
    #     G[edge[0]][edge[1]]
    # end3 = time.time()
    # print('time ',end1-start1)
    # print('time ', end2 - start2)
    # print('time ', end3 - start3)


    # G = nx.read_edgelist("mydata/test.txt", create_using=nx.DiGraph())
    # G_motif = nx.read_edgelist("mydata/motif/directed/motif4_3_0.txt", create_using=nx.DiGraph())
    G =nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    G.add_edges_from([(1, 2), (2, 3),(3,1),(2,4),(3,4)])

    g = nx.Graph()
    g.add_nodes_from([1, 2, 3])
    g.add_edges_from([(1, 2), (2, 3)])
    edgelist = list(nx.edges(G))
    node_list = list(nx.nodes(G))
    number = 0
    number1 = 0
    number2 = 0
    start3 = time.time()
    print(edge_motif_num(G, g,(2,1),directed=False, weighted=False))
    end3 = time.time()
    print('all motif ' 'time ', end3 - start3)

    # G = nx.Graph()
    # G.add_nodes_from([1, 2, 3, 4, 5])
    # G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 3), (3, 5)])
    # M5 = nx.Graph()
    # M5.add_nodes_from([1, 2, 3, 4])
    # M5.add_edges_from([(1, 2), (1, 3), (1, 4), (3, 4)])
    # M11 = nx.Graph()
    # M11.add_nodes_from([1, 2, 3, 4])
    # M11.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 4)])
    # edge1 = (3, 4)
    # a = edge_motif_num(G, M5, edge1, twoWay=True, weighted=False)
    # edge2 = (1, 3)
    # b = edge_motif_num(G, M11, edge2, twoWay=True, weighted=False)
    # print(a, b)