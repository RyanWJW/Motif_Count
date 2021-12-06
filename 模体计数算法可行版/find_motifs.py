import networkx as nx
import time
from collections import deque
import copy
"""为网络可视化模体上色，找到模体的节点"""

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
    return G2_node_list

def DFS_nodes(M, m_nodes, rat, n, minQ, MS, deep, work, candi,result):

    if deep == len(m_nodes):
        if minQ >work:
            minQ=work
            for i in range(deep):
                result[i] = MS[i]
        # print(MS,minQ,work)
        return result,minQ
    work1=0
    candi1=0
    for node in m_nodes:
        if node in MS[:deep]:
            continue
        candi1 = candi
        for node1 in MS[:deep]:
            if M.has_edge(node,node1):
                candi1=rat*candi1
        candi1=candi1*n
        work1 = n * candi - candi1 + work
        MS[deep]=node
        result, minQ= DFS_nodes(M, m_nodes, rat, n, minQ, MS, deep + 1, work1, candi1, result)
    return result,minQ

def Motif_node_sort(M,m_nodes,deeps):
    """
    找到一种最快的搜索顺序
    :param M:
    :param m_nodes:
    :param deeps:
    :return:
    """
    rat=0.5
    n=10
    minQ=99999999999999
    MS=['*' for x in range(len(m_nodes))]
    work=0
    candi=1
    m_nodes1=['*' for x in range(len(m_nodes))]
    if deeps==1:
        MS[0]=m_nodes[0]
    if deeps == 2:
        MS[0]=m_nodes[0]
        MS[1]=m_nodes[1]
    m_nodes1,minQ=DFS_nodes(M, m_nodes, rat, n, minQ, MS, deeps, work, candi,m_nodes1)
    return m_nodes1


def find_motif(G,Motif,G_node_list,G2_node_list,n_G2,MS,deeps,derepeat,weighted=False):
    # start = time.time()
    number = 0  # 存储模体数量
    deep = deeps
    SL=[]
    for i in range(n_G2-deeps):
        SL.append([])
        for j in range(0,n_G2-deeps-i):
            SL[i].append([])

    searchset = set(G_node_list)
    searchset = searchset - set(MS[0:deeps])
    for j in range(deeps, n_G2):
        SL[0][j - deeps] = searchset
    for i in range(deeps):
        ss = []
        neighbor1 = searchset & set(G.neighbors(MS[i]))
        neighbor2 = searchset - set(G.neighbors(MS[i]))
        for j in range(deeps, n_G2):
            hasEdge = Motif.has_edge(G2_node_list[i], G2_node_list[j])
            if (hasEdge):
                searchset1 = neighbor1
            else:
                searchset1 = neighbor2

            if weighted:
                for k in searchset1:
                    if (not Feasibility_weighted(G, Motif, G2_node_list[i], G2_node_list[j], MS[i], k,hasEdge)):
                        ss.append(k)
            searchset1=searchset1-set(ss)
            if (not searchset1):
                return 0
            if i == 0:
                SL[0][j-deeps] =  searchset1
            else:
                SL[0][j - deeps] = set(SL[0][j - deeps]) & searchset1

    if n_G2 - deeps < 2:
        return len(SL[0][0])
    Quelist = []
    for i in range(n_G2 - deeps):
        Quelist.append(deque())

    Quelist[deep - deeps].extend(SL[deep - deeps][0])
    ddd = False
    while (1):
        if deep == n_G2 - 1:
            number +=len(SL[deep-deeps][0])
            deep -= 1

        while (not Quelist[deep - deeps]):
            deep -= 1
            if deep < deeps:
                return number

        MS[deep] = Quelist[deep - deeps].pop()
        neighbor1 = set(G.neighbors(MS[deep]))
        for i in range(1,n_G2-deep):
            searchset = SL[deep-deeps][i]
            searchset = searchset - set(MS[0:deep+1])
            hasEdge= Motif.has_edge(G2_node_list[deep], G2_node_list[deep+i])
            if (hasEdge):
                searchset = searchset & neighbor1
            else:
                searchset = searchset - neighbor1

            if (not searchset):
                ddd = False
                break
            if derepeat[deep+i]!=-1 and derepeat[deep+i]<=deep:
                rrr=[]
                for k in list(searchset):
                    if int(k) <int(MS[derepeat[deep+i]]):
                        rrr.append(k)
                searchset= searchset - set(rrr)
            ss=[]
            if weighted:
                for k in searchset:
                    if (not Feasibility_weighted(G, Motif, G2_node_list[deep], G2_node_list[deep+i], MS[deep], k,hasEdge)):
                        ss.append(k)
            searchset = searchset-set(ss)
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

def find_motif_directed(G,Motif,G_node_list,G2_node_list,n_G2,MS,deeps,derepeat,weighted=False):
    # start = time.time()
    # print("@@@@@",G2_node_list)
    edgelist = list(nx.edges(G))
    edgelist1 = []
    for i in edgelist:
        edgelist1.append((i[1], i[0]))

    G2 = nx.DiGraph()
    G2.add_nodes_from(G_node_list)
    G2.add_edges_from(edgelist1)

    number = 0  # 存储模体数量
    deep = deeps
    SL=[]
    for i in range(n_G2-deeps):
        SL.append([])
        for j in range(0,n_G2-deeps-i):
            SL[i].append([])

    searchset = set(G_node_list) - set(MS[0:deeps])
    for j in range(deeps, n_G2):
        SL[0][j - deeps] = searchset

    for i in range(deeps):
        ss = []
        neighbor1 = searchset & set(G.neighbors(MS[i]))
        neighbor2 = searchset - set(G.neighbors(MS[i]))
        neighbor3 = searchset & set(G2.neighbors(MS[i]))
        neighbor4 = searchset - set(G2.neighbors(MS[i]))
        for j in range(deeps, n_G2):
            hasEdge = Motif.has_edge(G2_node_list[i], G2_node_list[j])
            hasEdge1 = Motif.has_edge(G2_node_list[j], G2_node_list[i])
            if (hasEdge):
                searchset1 = neighbor1
            else:
                searchset1 = neighbor2
            if (hasEdge1):
                searchset1 = searchset1 & neighbor3
            else:
                searchset1 = searchset1 & neighbor4
            if weighted:
                for k in searchset1:
                    if ( not Feasibility_weighted_directed(G, Motif, G2_node_list[i], G2_node_list[j], MS[i], k,hasEdge,hasEdge1)):
                        ss.append(k)
            searchset1=searchset1-set(ss)
            if (not searchset1):
                return 0

            if i == 0:
                SL[0][j - deeps] = searchset1
            else:
                SL[0][j - deeps] = set(SL[0][j - deeps]) & searchset1

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
        # if derepeat[deep] != -1:
        #     MS[deep] = Quelist[deep - deeps].pop()
        #
        #     while(int(MS[deep]) < int(MS[derepeat[deep]])):
        #         while (not Quelist[deep - deeps]):
        #             deep -= 1
        #             if deep < deeps:
        #                 return number
        #         MS[deep] = Quelist[deep - deeps].pop()
        #         if derepeat[deep] == -1:
        #             break
        # else:
        #     MS[deep] = Quelist[deep - deeps].pop()
        MS[deep] = Quelist[deep - deeps].pop()
        neighbor1 = set(G.neighbors(MS[deep]))
        neighbor2 = set(G2.neighbors(MS[deep]))
        for i in range(1,n_G2-deep):
            searchset = SL[deep-deeps][i]
            searchset = searchset - set(MS[0:deep+1])
            hasEdge= Motif.has_edge(G2_node_list[deep], G2_node_list[deep+i])
            hasEdge1 = Motif.has_edge(G2_node_list[deep+i], G2_node_list[deep])
            if (hasEdge):
                searchset = searchset & neighbor1
            else:
                searchset = searchset - neighbor1
            if (hasEdge1):
                searchset = searchset & neighbor2
            else:
                searchset = searchset - neighbor2

            if (not searchset):
                ddd = False
                break

            if derepeat[deep + i] != -1 and derepeat[deep + i] <= deep:
                rrr = []
                for k in list(searchset):
                    if int(k) < int(MS[derepeat[deep + i]]):
                        rrr.append(k)
                searchset = searchset - set(rrr)

            ss=[]
            if weighted:
                for k in searchset:
                    if ( not Feasibility_weighted_directed(G, Motif, G2_node_list[deep], G2_node_list[deep+i], MS[deep], k,hasEdge,hasEdge1)):
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



def combine_motif_list(motif_list,MS):
    ll=copy.deepcopy(list(MS))
    motif_list.append(ll)
    # print(motif_list)


def find_motif_list(G,Motif,G_node_list,G2_node_list,n_G2,MS,deeps,derepeat,weighted=False):
    # start = time.time()
    motif_list =[]
    number = 0  # 存储模体数量
    deep = deeps
    SL=[]
    for i in range(n_G2-deeps):
        SL.append([])
        for j in range(0,n_G2-deeps-i+1):
            SL[i].append([])

    searchset = set(G_node_list)
    searchset = searchset - set(MS[0:deeps])
    for j in range(deeps, n_G2):
        SL[0][j - deeps] = searchset

    for i in range(deeps):
        ss = []
        neighbor1 = searchset & set(G.neighbors(MS[i]))
        neighbor2 = searchset - set(G.neighbors(MS[i]))
        for j in range(deeps, n_G2):
            hasEdge=Motif.has_edge(G2_node_list[i], G2_node_list[j])
            if (hasEdge):
                searchset1 = neighbor1
            else:
                searchset1 = neighbor2

            if weighted:
                for k in searchset1:
                    if (not Feasibility_weighted(G, Motif, G2_node_list[i], G2_node_list[j], MS[i], k,hasEdge)):
                        ss.append(k)
            searchset1=searchset1-set(ss)
            if (not searchset1):
                return motif_list
            if i == 0:
                SL[0][j-deeps] =  searchset1
            else:
                SL[0][j - deeps] = set(SL[0][j - deeps]) & searchset1

    if n_G2 - deeps < 2:
        combine_motif_list(motif_list, MS)
        return motif_list
    Quelist = []
    for i in range(n_G2 - deeps):
        Quelist.append(deque())

    Quelist[deep - deeps].extend(SL[deep - deeps][0])
    ddd = False
    while (1):
        if deep > n_G2 - 1:
            deep -= 1
            number += len(SL[deep-deeps][0])
            combine_motif_list(motif_list,MS)

        while (not Quelist[deep - deeps]):
            deep -= 1
            if deep < deeps:
                return motif_list

        if derepeat[deep] != -1:
            MS[deep] = Quelist[deep - deeps].pop()
            while(int(MS[deep]) < int(MS[derepeat[deep]])):
                while (not Quelist[deep - deeps]):
                    deep -= 1
                    if deep < deeps:
                        return motif_list
                MS[deep] = Quelist[deep - deeps].pop()
                if derepeat[deep] == -1:
                    break
        else:
            MS[deep] = Quelist[deep - deeps].pop()
        neighbor1 = set(G.neighbors(MS[deep]))
        for i in range(1,n_G2-deep):
            searchset = set(SL[deep-deeps][i])
            searchset = searchset - set(MS[0:deep+1])
            hasEdge= Motif.has_edge(G2_node_list[deep], G2_node_list[deep+i])
            if (hasEdge):
                searchset = searchset & neighbor1
            else:
                searchset = searchset - neighbor1

            if (not searchset):
                ddd = False
                break
            ss=[]

            if weighted:
                for k in searchset:
                    if (not Feasibility_weighted(G, Motif, G2_node_list[deep], G2_node_list[deep+i], MS[deep], k,hasEdge)):
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
            if deep < n_G2:
                Quelist[deep - deeps].extend(SL[deep-deeps][0])

def find_motif_directed_list(G,Motif,G_node_list,G2_node_list,n_G2,MS,deeps,derepeat,weighted=False):
    # start = time.time()
    # print("@@@@@",G2_node_list)
    motif_list = []
    edgelist = list(nx.edges(G))
    edgelist1 = []
    for i in edgelist:
        edgelist1.append((i[1], i[0]))
    G2 = nx.DiGraph()
    G2.add_nodes_from(G_node_list)
    G2.add_edges_from(edgelist1)

    number = 0  # 存储模体数量
    deep = deeps
    SL=[]
    for i in range(n_G2-deeps):
        SL.append([])
        for j in range(0,n_G2-deeps-i+1):
            SL[i].append([])
    searchset = set(G_node_list) - set(MS[0:deeps])
    for j in range(deeps, n_G2):
        SL[0][j - deeps] = searchset
    for i in range(deeps):
        ss = []
        neighbor1 = searchset & set(G.neighbors(MS[i]))
        neighbor2 = searchset - set(G.neighbors(MS[i]))
        neighbor3 = searchset & set(G2.neighbors(MS[i]))
        neighbor4 = searchset - set(G2.neighbors(MS[i]))
        for j in range(deeps, n_G2):
            hasEdge=Motif.has_edge(G2_node_list[i], G2_node_list[j])
            hasEdge1 = Motif.has_edge(G2_node_list[j], G2_node_list[i])
            if (hasEdge):
                searchset1 = neighbor1
            else:
                searchset1 = neighbor2
            if (hasEdge1):
                searchset1 = searchset1 & neighbor3
            else:
                searchset1 = searchset1 & neighbor4
            if weighted:
                for k in searchset1:
                    if ( not Feasibility_weighted_directed(G, Motif, G2_node_list[i], G2_node_list[j], MS[i], k,hasEdge,hasEdge1)):
                        ss.append(k)
            searchset1=searchset1-set(ss)
            if (not searchset1):
                return motif_list
            if i == 0:
                SL[0][j-deeps]=  searchset1
            else:
                SL[0][j - deeps] = set(SL[0][j - deeps]) & searchset1
    if n_G2 - deeps < 2:
        combine_motif_list(motif_list, MS)
        return motif_list
        # return SL[0][0]
    Quelist = []
    for i in range(n_G2 - deeps):
        Quelist.append(deque())

    Quelist[deep - deeps].extend(SL[deep - deeps][0])
    ddd = False
    while (1):
        if  deep > n_G2 - 1:
            deep -= 1
            number += len(SL[deep-deeps][0])
            combine_motif_list(motif_list, MS)
        while (not Quelist[deep - deeps]):
            deep -= 1
            if deep < deeps:
                return motif_list

        if derepeat[deep] != -1:
            MS[deep] = Quelist[deep - deeps].pop()

            while(int(MS[deep]) < int(MS[derepeat[deep]])):
                while (not Quelist[deep - deeps]):
                    deep -= 1
                    if deep < deeps:
                        return number
                MS[deep] = Quelist[deep - deeps].pop()
                if derepeat[deep] == -1:
                    break
        else:
            MS[deep] = Quelist[deep - deeps].pop()
        neighbor1 = set(G.neighbors(MS[deep]))
        neighbor2 = set(G2.neighbors(MS[deep]))
        for i in range(1,n_G2-deep):
            searchset = SL[deep-deeps][i]
            searchset = searchset - set(MS[0:deep+1])
            hasEdge= Motif.has_edge(G2_node_list[deep], G2_node_list[deep+i])
            hasEdge1 = Motif.has_edge(G2_node_list[deep+i], G2_node_list[deep])
            if (hasEdge):
                searchset = searchset & neighbor1
            else:
                searchset = searchset - neighbor1
            if (hasEdge1):
                searchset = searchset & neighbor2
            else:
                searchset = searchset - neighbor2

            if (not searchset):
                ddd = False
                break
            ss=[]
            if weighted:
                for k in searchset:
                    if ( not Feasibility_weighted_directed(G, Motif, G2_node_list[deep], G2_node_list[deep+i], MS[deep], k,hasEdge,hasEdge1)):
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
            if deep < n_G2:
                Quelist[deep - deeps].extend(SL[deep-deeps][0])


def get_node_group(G2_node_list,n_G2,repetitions):
    nodes_group={}
    for i in G2_node_list:
        nodes_group[i]={}
        for j in G2_node_list:
            nodes_group[i][j]=-1
    for i in range(n_G2):
        for j in range(len(repetitions)):
            for k in range(len(repetitions)):
                nodes_group[repetitions[j][i]][repetitions[k][i]] = 1
                nodes_group[repetitions[k][i]][repetitions[j][i]] = 1
    return nodes_group

def Build_Motif_Tree(motif):
    motif_tree={}
    mark={}
    nodelist=list(nx.nodes(motif))
    for i in nodelist:
        mark[i]=0
        motif_tree[i]=[]
    mark[nodelist[0]]=1
    build_tree(motif,mark,nodelist[0],motif_tree)
    return motif_tree

def build_tree(motif,mark,node,motif_tree):
    a=list(motif.neighbors(node))
    b=[]
    for i in a:
        if mark[i] ==0:
            b.append(i)
            mark[i]=1
    # if b==[]:
    #     return
    motif_tree[node]=b
    for i in motif_tree[node]:
        build_tree(motif,mark,i,motif_tree)

#
# def get_prevent_repetition_list(motif,G2_node_list,len1,MS,deep, weighted,derepet):
#     repetitions= find_motif_list(motif,motif, G2_node_list, G2_node_list, len1, MS, deep,derepet, weighted)
#     if len(repetitions)==1:
#         return derepet
#     nodes_group = get_node_group(G2_node_list,len1,repetitions)
#     for i in range(len1):
#         k=-1
#         s=0
#         for j in range(len1):
#             if(nodes_group[G2_node_list[i]][G2_node_list[j]]==1 and derepet[j]==-1):
#                 derepet[j]=k
#                 k=j
#                 s+=1
#         if(s>1):
#             break
#     # print(derepet)
#     return get_prevent_repetition_list(motif, G2_node_list, len1, MS, deep, weighted,derepet)


def get_prevent_repetition_list(motif,G2_node_list,len1,repetitions):
    nodes_group = get_node_group(G2_node_list,len1,repetitions)
    motif_tree = Build_Motif_Tree(motif)
    mapnodelist={}
    for i in range(len(G2_node_list)):
        mapnodelist[G2_node_list[i]]=i

    derepet = [-1 for i in range(len1)]
    mark={}
    for i in G2_node_list:
        mark[i]=0
    for node in G2_node_list:
        for i in range(len(motif_tree[node])):
            if mark[motif_tree[node][i]]== 0:
                aaa=[]
                aaa.append(motif_tree[node][i])
                mark[motif_tree[node][i]] = 1
                for j in range(len(motif_tree[node])):
                    if i < j:
                        if nodes_group[motif_tree[node][i]][motif_tree[node][j]] == 1:
                            aaa.append(motif_tree[node][j])
                            mark[motif_tree[node][j]]=1
                bbb=[]
                for k in G2_node_list:
                    if k in aaa:
                        bbb.append(k)
                for k in range(len(bbb)):
                    if k==0:
                        continue
                    derepet[mapnodelist[bbb[k]]]=mapnodelist[bbb[k-1]]

    return derepet


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
    # G2_node_list[1:len1]=preSort(G_motif, G2_node_list[1:len1])  # 调整搜索顺序
    G2_node_list = Motif_node_sort(G_motif, G2_node_list, 1)
    MS = ['*' for x in range(len1)]
    node_motif_number = 0
    if directed:
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        derepeat = [-1 for i in range(len1)]
        repetitions = find_motif_directed_list(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 1, derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list, len1, repetitions)
        # 下面查找node节点的模体数
        MS[0] = node
        node_motif_number = find_motif_directed(G, G_motif, G_node_list, G2_node_list, len1, MS, 1, derepeat, weighted)
        # MS[0] = G2_node_list[0]
        # a = find_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 1, derepeat, weighted)
    else:
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        derepeat = [-1 for i in range(len1)]
        repetitions = find_motif_list(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 1, derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list, len1, repetitions)
        # 下面查找node节点的模体数
        MS[0] = node
        node_motif_number = find_motif(G, G_motif, G_node_list, G2_node_list, len1, MS, 1, derepeat, weighted)
        # MS[0] = G2_node_list[0]
        # a = find_motif(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 1, derepeat, weighted)
    # end = time.time()
    # print("node_motif_num总共用时{}秒".format((end - start)))
    #结果是需要除以重复的数
    return node_motif_number

def edge_motif_num(G,G_motif,edge,directed=False,weighted=False):
    """
        计算node节点作为模体的第一个节点所参与的模体数量
        :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
        :param G_motif: 模体图,可以有向或者无向但必须与图G一致
        :param edge: 图G中的一条边
        :param directed: 是否是有向图，是有向图值为True，否则为False，默认为无向图False
        :param weighted: 是否具有权重，是否是加权网络，若是值为True，若否值为False，默认为False,符号网络视为加权网络。
        :return :返回值是边模体数
    """
    # if directed:
    #     twoWay = False
    #     if not G.has_edge(edge[0], edge[1]):
    #         print("There is no such edge in the network.",edge)
    #         return 0
    #     if G.has_edge(edge[1], edge[0]):
    #         twoWay = True
    # else :
    #     twoWay =True

    twoWay = False
    if (not G.has_edge(edge[0], edge[1])) and (not G.has_edge(edge[1], edge[0])):
        print("There is no such edge in the network.")
        twoWay = True
    if G.has_edge(edge[1], edge[0]) and G.has_edge(edge[0], edge[1]):
        twoWay = True

    # start = time.time()
    G_node_list = list(nx.nodes(G))
    G2_node_list = list(nx.nodes(G_motif))
    len1 = len(G2_node_list)
    # G2_node_list[2:len1]=preSort(G_motif, G2_node_list[2:len1])  # 调整搜索顺序
    G2_node_list = Motif_node_sort(G_motif, G2_node_list, 2)
    MS = ['*' for x in range(len1)]
    edge_motif_number=0

    if directed:

        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        MS[1] = G2_node_list[1]
        derepeat = [-1 for i in range(len1)]
        repetitions = find_motif_directed_list(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list,len1, repetitions)
        # 计算边模体数量01的顺序不同
        MS[0] = edge[0]
        MS[1] = edge[1]
        edge_motif_number = find_motif_directed(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
        MS[0] = G2_node_list[0]
        MS[1] = G2_node_list[1]
        a = find_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
        if twoWay:  # 如果是双向边还需要查找反方向的模体数
            MS[0] = edge[1]
            MS[1] = edge[0]
            edge_motif_number += find_motif_directed(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
            MS[0] = G2_node_list[1]
            MS[1] = G2_node_list[0]
            a += find_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)

    else:

        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        MS[0] = G2_node_list[0]
        MS[1] = G2_node_list[1]
        derepeat = [-1 for i in range(len1)]
        repetitions = find_motif_list(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list, len1, repetitions)
        #------------------------------#
        MS[0] = edge[0]
        MS[1] = edge[1]
        edge_motif_number= find_motif(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
        MS[0] = G2_node_list[0]
        MS[1] = G2_node_list[1]
        a = find_motif(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
        if twoWay:  # 如果是双向边还需要查找反方向的模体数
            MS[0] = edge[1]
            MS[1] = edge[0]
            edge_motif_number += find_motif(G, G_motif, G_node_list, G2_node_list, len1, MS, 2, derepeat,weighted)
            MS[0] = G2_node_list[1]
            MS[1] = G2_node_list[0]
            a += find_motif(G_motif, G_motif, G2_node_list, G2_node_list, len1, MS, 2, derepeat, weighted)
    # end = time.time()
    # print("edge_motif_num总共用时{}秒".format((end - start)))
    # 结果是需要除以重复的数
    return edge_motif_number/a


def total_motif_num(G,G_motif,directed=False,weighted=False):
    """
        计算模体总数
        :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
        :param G_motif: 模体图,可以有向或者无向但类型必须与图G一致
        :param directed: 是否是有向图，是有向图值为True，否则为False，默认为无向图False
        :param weighted: 是否具有权重，是否是加权网络，若是值为True，若否值为False，默认为False,符号网络视为加权网络。
        :return :返回值是模体总数
    """
    G_node_list = list(nx.nodes(G))
    G2_node_list = list(nx.nodes(G_motif))
    n_G2 = len(G2_node_list)
    # start = time.time()

    # G2_node_list=preSort(G_motif, G2_node_list)  # 调整搜索顺序
    G2_node_list = Motif_node_sort(G_motif, G2_node_list,0)

    MS = ['*' for x in range(n_G2)]
    total_motif_number = 0
    # repetitions = 0
    # 计算模体总数量
    if directed:
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        derepeat = [-1 for i in range(n_G2)]
        repetitions = find_motif_directed_list(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list, n_G2, repetitions)
        total_motif_number = find_motif_directed(G, G_motif, G_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
        a=find_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)

    else:
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        derepeat = [-1 for i in range(n_G2)]
        repetitions = find_motif_list(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0,derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list, n_G2, repetitions)
        print(derepeat)
        total_motif_number = find_motif(G, G_motif, G_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
        a = find_motif(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
        print(a)
        # print(total_motif_number)
    # end = time.time()
    # print("total_motif_num总共用时{}秒".format((end - start)))
    # 结果是需要除以重复的数
    return total_motif_number/a



def total_motif_list(G,G_motif,directed=False,weighted=False):
    """
        计算模体总数
        :param G: 图或（网络），可以是有向或无向图，是networkx.Graph() 或 networkx.DiGraph()
        :param G_motif: 模体图,可以有向或者无向但类型必须与图G一致
        :param directed: 是否是有向图，是有向图值为True，否则为False，默认为无向图False
        :param weighted: 是否具有权重，是否是加权网络，若是值为True，若否值为False，默认为False,符号网络视为加权网络。
        :return :返回值是模体总数
    """
    G_node_list = list(nx.nodes(G))
    G2_node_list = list(nx.nodes(G_motif))
    n_G2 = len(G2_node_list)
    # start = time.time()

    # G2_node_list=preSort(G_motif, G2_node_list)  # 调整搜索顺序
    G2_node_list = Motif_node_sort(G_motif, G2_node_list,0)

    MS = ['*' for x in range(n_G2)]


    # 计算模体总数量
    if directed:
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        derepeat = [-1 for i in range(n_G2)]
        repetitions = find_motif_directed_list(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list, n_G2, repetitions)
        total_motif = find_motif_directed_list(G, G_motif, G_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
        # a=find_motif_directed(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)

    else:
        # 搜索模体图中的模体数，如果大于1，说明有对称结构导致重复计算。
        derepeat = [-1 for i in range(n_G2)]
        repetitions = find_motif_list(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0,derepeat, weighted)
        derepeat = get_prevent_repetition_list(G_motif, G2_node_list, n_G2, repetitions)
        # print(derepeat)
        total_motif = find_motif_list(G, G_motif, G_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
        # a = find_motif_list(G_motif, G_motif, G2_node_list, G2_node_list, n_G2, MS, 0, derepeat, weighted)
    # print(a)
    motif_set=[]
    for i in range(len(total_motif)):
        ss=""
        for j in sorted(total_motif[i]):
            ss=ss+str(j)+"_"
        motif_set.append((ss,i))
    motif_str=sorted(motif_set,key=lambda student: student[0])

    # print(motif_str)
    motifss=[]
    motifss.append(total_motif[motif_str[0][1]])
    for i in range(1,len(total_motif)):
        if motif_str[i][0] != motif_str[i-1][0]:
            motifss.append(total_motif[motif_str[i][1]])
    print(len(motifss))
    motif_edge=[]
    for i in range(len(motifss)):
        motif_edge.append([])
    if directed:
        for i in range(len(G2_node_list)):
            for j in  range(len(G2_node_list)):
                if(i!=j):
                    if(G_motif.has_edge(G2_node_list[i],G2_node_list[j])):
                        for k in range(len(motifss)):
                            motif_edge[k].append((motifss[k][i],motifss[k][j]))
    else:
        for i in range(len(G2_node_list)):
            for j in range(len(G2_node_list)):
                if (j>i):
                    if(G_motif.has_edge(G2_node_list[i],G2_node_list[j])):
                        for k in range(len(motifss)):
                            motif_edge[k].append((motifss[k][i],motifss[k][j]))
    # print(motif_edge)
    return motifss,motif_edge





if __name__ == "__main__":

    G = nx.read_edgelist("mydata/USAir97.txt", create_using=nx.Graph())
    # G_motif = nx.read_edgelist("mydata/motif/directed/motif4_3_0.txt", create_using=nx.DiGraph())
    g = nx.Graph()
    # g.add_nodes_from([1, 2, 3, 4,5,6,7])
    # g.add_edges_from([(1, 2), (1, 3), (2, 4),(2,5),(3,6),(3,7)])
    # g.add_nodes_from([1, 2, 3, 4])
    # g.add_edges_from([(1, 2), (1, 3), (3, 4),(2,4)])
    g.add_nodes_from([1, 2, 3])
    g.add_edges_from([(1, 2), (1, 3),  (2, 3)])
    edgelist = list(nx.edges(G))
    node_list = list(nx.nodes(G))
    number = 0
    number1 = 0
    number2 = 0
    start3 = time.time()
    motif_nodes,motif_edges=total_motif_list(G, g, directed=False, weighted=False)
    end3 = time.time()
    print('all motif time ', end3 - start3)