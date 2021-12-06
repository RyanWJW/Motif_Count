import networkx as nx
import time


class motif:
    """
    树形模体类，模体种类数是
    """
    def __init__(self):
        self.M2_1 = nx.from_edgelist([(1, 2)], create_using=nx.DiGraph())
        self.M3_1 = nx.from_edgelist([(1, 2), (1, 3)], create_using=nx.DiGraph())
        self.M3_2 = nx.from_edgelist([(1, 2), (2, 3)], create_using=nx.DiGraph())
        self.M4_1 = nx.from_edgelist([(1, 2), (1, 3), (1, 4)], create_using=nx.DiGraph())
        self.M4_2 = nx.from_edgelist([(1, 2), (2, 3), (2, 4)], create_using=nx.DiGraph())
        self.M4_3 = nx.from_edgelist([(1, 2), (1, 3), (2, 4)], create_using=nx.DiGraph())
        self.M4_4 = nx.from_edgelist([(1, 2), (2, 3), (3, 4)], create_using=nx.DiGraph())
        self.M5_1 = nx.from_edgelist([(1, 2), (1, 3), (1, 4), (1, 5)], create_using=nx.DiGraph())
        self.M5_2 = nx.from_edgelist([(1, 2), (2, 3), (3, 4), (4, 5)], create_using=nx.DiGraph())
        self.M5_3 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (3, 5)], create_using=nx.DiGraph())
        self.M5_4 = nx.from_edgelist([(1, 2), (1, 3), (1, 4), (2, 5)], create_using=nx.DiGraph())
        self.M5_5 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (2, 5)], create_using=nx.DiGraph())
        self.M5_6 = nx.from_edgelist([(1, 2), (2, 3), (2, 4), (2, 5)], create_using=nx.DiGraph())
        self.M5_7 = nx.from_edgelist([(1, 2), (2, 3), (2, 4), (3, 5)], create_using=nx.DiGraph())
        self.M5_8 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (4, 5)], create_using=nx.DiGraph())
        self.M5_9 = nx.from_edgelist([(1, 2), (2, 3), (3, 4), (3, 5)], create_using=nx.DiGraph())
        self.M6_1 = nx.from_edgelist([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)], create_using=nx.DiGraph())
        self.M6_2 = nx.from_edgelist([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], create_using=nx.DiGraph())
        self.M6_3 = nx.from_edgelist([(1, 2), (1, 3), (1, 4), (1, 5), (2, 6)], create_using=nx.DiGraph())
        self.M6_4 = nx.from_edgelist([(1, 2), (2, 3), (2, 4), (2, 5), (2, 6)], create_using=nx.DiGraph())
        self.M6_5 = nx.from_edgelist([(1, 2), (1, 3), (1, 4), (2, 5), (5, 6)], create_using=nx.DiGraph())
        self.M6_6 = nx.from_edgelist([(1, 2), (2, 3), (2, 4), (2, 5), (3, 6)], create_using=nx.DiGraph())
        self.M6_7 = nx.from_edgelist([(1, 2), (2, 3), (3, 4), (3, 5), (3, 6)], create_using=nx.DiGraph())
        self.M6_8 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (4, 5), (5, 6)], create_using=nx.DiGraph())
        self.M6_9 = nx.from_edgelist([(1, 2), (2, 3), (2, 4), (3, 5), (5, 6)], create_using=nx.DiGraph())
        self.M6_10 = nx.from_edgelist([(1, 2), (2, 3), (3, 4), (3, 5), (4, 6)], create_using=nx.DiGraph())
        self.M6_11 = nx.from_edgelist([(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)], create_using=nx.DiGraph())
        self.M6_12 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (2, 5), (4, 6)], create_using=nx.DiGraph())
        self.M6_13 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (4, 5), (4, 6)], create_using=nx.DiGraph())
        self.M6_14 = nx.from_edgelist([(1, 2), (2, 3), (2, 4), (3, 5), (3, 6)], create_using=nx.DiGraph())
        self.M6_15 = nx.from_edgelist([(1, 2), (1, 3), (1, 4), (2, 5), (2, 6)], create_using=nx.DiGraph())
        self.M6_16 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (2, 5), (2, 6)], create_using=nx.DiGraph())
        self.M6_17 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)], create_using=nx.DiGraph())
        self.M6_18 = nx.from_edgelist([(1, 2), (1, 3), (1, 4), (2, 5), (3, 6)], create_using=nx.DiGraph())
        self.M6_19 = nx.from_edgelist([(1, 2), (1, 3), (2, 4), (3, 5), (4, 6)], create_using=nx.DiGraph())
        self.M6_20 = nx.from_edgelist([(1, 2), (2, 3), (2, 4), (3, 5), (4, 6)], create_using=nx.DiGraph())

        self.MO=[]
        self.MO.append(self.M2_1)
        self.MO.append(self.M3_1)
        self.MO.append(self.M3_2)
        self.MO.append(self.M4_1)
        self.MO.append(self.M4_2)
        self.MO.append(self.M4_3)
        self.MO.append(self.M4_4)
        self.MO.append(self.M5_1)
        self.MO.append(self.M5_2)
        self.MO.append(self.M5_3)
        self.MO.append(self.M5_4)
        self.MO.append(self.M5_5)
        self.MO.append(self.M5_6)
        self.MO.append(self.M5_7)
        self.MO.append(self.M5_8)
        self.MO.append(self.M5_9)
        self.MO.append(self.M6_1)
        self.MO.append(self.M6_2)
        self.MO.append(self.M6_3)
        self.MO.append(self.M6_4)
        self.MO.append(self.M6_5)
        self.MO.append(self.M6_6)
        self.MO.append(self.M6_7)
        self.MO.append(self.M6_8)
        self.MO.append(self.M6_9)
        self.MO.append(self.M6_10)
        self.MO.append(self.M6_11)
        self.MO.append(self.M6_12)
        self.MO.append(self.M6_13)
        self.MO.append(self.M6_14)
        self.MO.append(self.M6_15)
        self.MO.append(self.M6_16)
        self.MO.append(self.M6_17)
        self.MO.append(self.M6_18)
        self.MO.append(self.M6_19)
        self.MO.append(self.M6_20)


def C(a,b):
    if(b==0):
        return 1
    k=0
    s1=1
    s2=1
    while(1):
        s2=s2*(a-k)
        k=k+1
        s1 = s1 * k
        if(b<=k):
            break
    return s2/s1


def A(a):
    result=1
    while(1):
        if(a<=1):
            break
        result= result * a
        a=a-1
    return result


def DFS(subgraph,m,n,MS,deep):
    # print(deep)
    result=0
    tag=True
    for i in range(n):
        for j in range(deep):
            if i==MS[j]:
                tag=False
                break
        if not tag:
            tag=True
            continue
        else:
            MS[deep]=i
            if deep==m-1:
                ss=1
                for k in range(m):
                    ss=ss*subgraph[k][MS[k]]
                result+=ss
            else:
                result+= DFS(subgraph, m, n, MS, deep+1)
    # print("_____",result)
    return result


def is_parent_of_leaf(G,node):
    node_list=list(G.neighbors(node))
    for i in node_list:
        if(G.out_degree(i)!=0):
            return False
    return True

def has_parent_of_leaf(G,node):
    node_list=list(G.neighbors(node))
    for i in node_list:
        if(G.out_degree(i)==0):
            return True
    return False


def treemotif(G,node,motif,gnode):
    if motif.out_degree(gnode) > G.out_degree(node):
        return 0
    if list(motif.neighbors(gnode))==[]:
        return 1
    if(is_parent_of_leaf(motif,gnode)):
        a=G.out_degree(node)
        b=motif.out_degree(gnode)
        return C(a,b)

    if(has_parent_of_leaf(motif,gnode)):
        node_list = list(motif.neighbors(gnode))
        gnodelist = []
        x=0
        y=0

        for i in node_list:
            if motif.out_degree(i) == 0:
                y+=1
            else:
                x+=1
                gnodelist.append(i)

        nodelist = list(G.neighbors(node))
        subgraph = {}
        m = len(gnodelist)
        n = len(nodelist)

        for i in range(m):  # 计算所有子节模体的个数
            subgraph[i] = {}
            for j in range(n):
                subgraph[i][j] = treemotif(G, nodelist[j], motif, gnodelist[i])
        MS = ["*" for i in range(m)]
        result = DFS(subgraph, m, n, MS, 0)
        result*=C(n-x,y)
        return result

    nodelist=list(G.neighbors(node))
    gnodelist = list(motif.neighbors(gnode))
    subgraph={}
    m=len(gnodelist)
    n=len(nodelist)
    for i in range(m):#计算所有子节模体的个数
        subgraph[i]={}
        for j in range(n):
            subgraph[i][j]=treemotif(G,nodelist[j], motif, gnodelist[i])
    MS = ["*" for i in range(m)]
    result =DFS(subgraph, m, n, MS, 0)
    # print(result)
    return result




def treemotif2(G,node,motif,k,gnode,allmotifs,node_nums,SM):
    if motif.MO[k].out_degree(gnode) > G.out_degree(node):
        return 0
    if list(motif.MO[k].neighbors(gnode))==[]:
        return 1
    if is_parent_of_leaf(motif.MO[k],gnode):
        a=G.out_degree(node)
        b=motif.MO[k].out_degree(gnode)
        return C(a,b)

    if has_parent_of_leaf(motif.MO[k],gnode):
        node_list = list(motif.MO[k].neighbors(gnode))
        gnodelist = []
        x=0
        y=0

        for i in node_list:
            if motif.MO[k].out_degree(i) == 0:
                y+=1
            else:
                x+=1
                gnodelist.append(i)

        nodelist = list(G.neighbors(node))
        subgraph = {}
        m = len(gnodelist)
        n = len(nodelist)
        for i in range(m):  # 计算所有子节模体的个数
            subgraph[i] = {}
            for j in range(n):
                subgraph[i][j] = allmotifs[SM[gnodelist[i]]][nodelist[j]]
            # if is_parent_of_leaf(motif.MO[k],gnodelist[i]) :
            #     for j in range(n):
            #         subgraph[i][j] = treemotif(G, nodelist[j], motif.MO[k], gnodelist[i])
            # else:
            #     if node_nums[gnodelist[i]]<=3:
            #         for j in range(n):
            #             subgraph[i][j] = treemotif(G, nodelist[j], motif.MO[k], gnodelist[i])
            #     else:
            #         for j in range(n):
            #             subgraph[i][j] = allmotifs[SM[gnodelist[i]]][nodelist[j]]

        MS = ["*" for i in range(m)]
        result = DFS(subgraph, m, n, MS, 0)
        result*=C(n-x,y)
        return result

    nodelist=list(G.neighbors(node))
    gnodelist = list(motif.MO[k].neighbors(gnode))
    subgraph={}
    m=len(gnodelist)
    n=len(nodelist)
    for i in range(m):#计算所有子节模体的个数
        subgraph[i]={}
        for j in range(n):
            subgraph[i][j] = allmotifs[SM[gnodelist[i]]][nodelist[j]]
        # if is_parent_of_leaf(motif.MO[k], gnodelist[i]):
        #     for j in range(n):
        #         subgraph[i][j] = treemotif(G, nodelist[j], motif.MO[k], gnodelist[i])
        # else:
        #     if node_nums[gnodelist[i]] <= 3:
        #         for j in range(n):
        #             subgraph[i][j] = treemotif(G, nodelist[j], motif.MO[k], gnodelist[i])
        #     else:
        #         for j in range(n):
        #             subgraph[i][j] = allmotifs[SM[gnodelist[i]]][nodelist[j]]
    MS = ["*" for i in range(m)]
    result =DFS(subgraph, m, n, MS, 0)
    # print(result)
    return result


def treemotif3(G,node,motif,gnode):
    if motif.out_degree(gnode) != G.out_degree(node):
        return 0
    if list(motif.neighbors(gnode))==[]:
        return 1
    if(is_parent_of_leaf(motif,gnode)):
        return 1

    if(has_parent_of_leaf(motif,gnode)):
        node_list = list(motif.neighbors(gnode))
        gnodelist = []
        x=0
        y=0
        for i in node_list:
            if motif.out_degree(i) == 0:
                y+=1
            else:
                x+=1
                gnodelist.append(i)

        nodelist = list(G.neighbors(node))
        nodelist1 = []

        x1=0
        y1=0
        for i in nodelist:
            if G.out_degree(i) == 0:
                y1+=1
            else:
                x1+=1
                nodelist1.append(i)
        if(y1!=y):
            return 0
        subgraph = {}
        m = len(gnodelist)
        n = len(nodelist1)
        for i in range(m):  # 计算所有子节模体的个数
            subgraph[i] = {}
            for j in range(n):
                subgraph[i][j] = treemotif3(G, nodelist1[j], motif, gnodelist[i])
        MS = ["*" for i in range(m)]
        result = DFS(subgraph, m, n, MS, 0)
        # result*=C(n-x,y)
        return result

    nodelist=list(G.neighbors(node))
    gnodelist = list(motif.neighbors(gnode))
    subgraph={}
    m=len(gnodelist)
    n=len(nodelist)
    for i in range(m):#计算所有子节模体的个数
        subgraph[i]={}
        for j in range(n):
            subgraph[i][j]=treemotif3(G,nodelist[j], motif, gnodelist[i])
    MS = ["*" for i in range(m)]
    result =DFS(subgraph, m, n, MS, 0)
    # print(result)
    return result


def motifnum(G,g):
    node_list = list(nx.nodes(G))
    result=0
    gnode=list(nx.nodes(g))
    for i in node_list:
        result +=treemotif(G,i,g,gnode[0])
    return result


def sub_motifnum(G,g,node):
    node_list = list(nx.nodes(G))
    result = 0
    for i in node_list:
        result += treemotif(G, i, g, node)
    return result

def sub_motif_num(G,g,node):
    return sub_motifnum(G, g, node) / treemotif(g,node, g,node)


def node_num(G,node,node_nums):
    if G.out_degree(node)==0:
        node_nums[node] = 1
        return 0
    Gnodel= list(G.neighbors(node))
    result=len(Gnodel)
    for i in range(len(Gnodel)):
        result+=node_num(G, Gnodel[i],node_nums)
    node_nums[node]=result+1
    return result

def sub_motif_num2(G,g,node,node_num):
    node_list = list(nx.nodes(G))
    if node_num != len(node_list):
        return 0
    if G.out_degree(node_list[0]) != g.out_degree(node):
        return 0

    return treemotif3(G, node_list[0], g, node)


def motif_num(G,motif):
    """
    计算模体数
    :param G: 网络
    :param motif: 模体
    :return: 模体数
    """
    return motifnum(G, motif) / motifnum(motif, motif)


def motifnum2(G, g, k, allmotifs):
    gnode = list(nx.nodes(g.MO[k]))
    node_nums ={}
    node_num(g.MO[k],gnode[0],node_nums)
    node_list = list(G.nodes)
    result=0
    allmotifs[k]={}
    SM={}
    for i in list(g.MO[k].neighbors(gnode[0])):
        for mo in range(k):
            if (sub_motif_num2(g.MO[mo], g.MO[k], i, node_nums[i]) > 0):
                SM[i]=mo
    for i in node_list:
        re = node_motifnum2(G, g, k, i, allmotifs,node_nums,SM)
        allmotifs[k][i] = re
        result += re
    return result


def motif_num2(G,motif,k,allmotifs):
    """
    计算模体数
    :param G: 网络
    :param motif: 模体
    :return: 模体数
    """
    return motifnum2(G, motif, k, allmotifs) / motifnum(motif.MO[k], motif.MO[k])

def node_motifnum2(G,g,k,node,allmotifs,node_nums,SM):
    gnode = list(nx.nodes(g.MO[k]))
    result= treemotif2(G, node, g, k, gnode[0],allmotifs,node_nums,SM)
    return result


def node_motif_num2(G,motif,k,node,allmotifs,SM):
    """
    计算节点模体数
    :param G: 网络
    :param motif: 模体
    :param node: 网络中的节点
    :return: 网络中node节点作为模体的第一个节点参与构成模体的模体数
    """
    return node_motifnum2(G, motif,k, node,allmotifs,SM) / motifnum(motif.MO[k], motif.MO[k])





def node_motifnum(G,g,node):
    gnode = list(nx.nodes(g))
    result= treemotif(G, node, g, gnode[0])
    return result


def node_motif_num(G,motif,node):
    """
    计算节点模体数
    :param G: 网络
    :param motif: 模体
    :param node: 网络中的节点
    :return: 网络中node节点作为模体的第一个节点参与构成模体的模体数
    """
    return node_motifnum(G, motif, node) / motifnum(motif, motif)



###################################################



def all_motif_num2(G):
    g = motif()
    allmotifs = {}
    allmotifs[0]={}
    for i in list(G.nodes):
        allmotifs[0][i]=G.out_degree(i)
    result = []
    for i in range(1, len(g.MO)):
        result.append(motif_num2(G, g, i, allmotifs))
    return result


def all_motif_num(G):
    """
    输出 所有模体数
    :param G: 网络
    """
    g = motif()
    # t0=time.time()
    # ss =motif_num(G, g.M3_1)
    # print("M3_1  ",ss)
    # t1=time.time()
    # print("time",t1-t0)
    # ss1 = motif_num(G, g.M3_2)
    # print("M3_2  ",ss1)
    # t2 = time.time()
    # print("time", t2 - t1)
    # ss2 = motif_num(G, g.M4_1)
    # print("M4_1  ",ss2)
    # t3 = time.time()
    # print("time", t3 - t2)
    # ss3 = motif_num(G, g.M4_2)
    # print("M4_2  ",ss3)
    # t4 = time.time()
    # print("time", t4 - t3)
    # ss4 = motif_num(G, g.M4_3)
    # print("M4_3  ",ss4)
    # t5 = time.time()
    # print("time", t5 - t4)
    # ss5 = motif_num(G, g.M4_4)
    # print("M4_4  ",ss5)
    # t6 = time.time()
    # print("time", t6 - t5)
    # ss6 = motif_num(G, g.M5_1)
    # print("M5_1  ",ss6)
    # t7 = time.time()
    # print("time", t7 - t6)
    # ss7 = motif_num(G, g.M5_2)
    # print("M5_2  ",ss7)
    # t8 = time.time()
    # print("time", t8 - t7)
    # ss8 = motif_num(G, g.M5_3)
    # print("M5_3  ",ss8)
    # t9 = time.time()
    # print("time", t9 - t8)
    # ss9 = motif_num(G, g.M5_4)
    # print("M5_4  ",ss9)
    # t10 = time.time()
    # print("time", t10 - t9)
    # ss10 = motif_num(G, g.M5_5)
    # print("M5_5  ",ss10)
    # t11 = time.time()
    # print("time", t11 - t10)
    # ss11 = motif_num(G, g.M5_6)
    # print("M5_6  ",ss11)
    # t12 = time.time()
    # print("time", t12 - t11)
    # ss12 = motif_num(G, g.M5_7)
    # print("M5_7  ",ss12)
    # t13 = time.time()
    # print("time", t13 - t12)
    # ss13 = motif_num(G, g.M5_8)
    # print("M5_8  ",ss13)
    # t14 = time.time()
    # print("time", t14 - t13)
    # ss14 = motif_num(G, g.M5_9)
    # print("M5_9  ",ss14)
    # t15 = time.time()
    # print("time", t15 - t14)
    result=[]
    for i in range(1,len(g.MO)):
        result.append(motif_num(G, g.MO[i]))
    return result

def K_motif_num(G,k):
    """
    输出 K阶模体数
    :param G: 网络
    :param k: 模体节点数

    """
    g = motif()
    result=[]
    if k==3:
        # ss = motif_num(G, g.M3_1)
        # print("M3_1  ", ss)
        # ss1 = motif_num(G, g.M3_2)
        # print("M3_2  ", ss1)
        for i in range(1,3):
            result.append(motif_num(G, g.MO[i]))
        return result
    if k==4:
        # ss2 = motif_num(G, g.M4_1)
        # print("M4_1  ", ss2)
        # ss3 = motif_num(G, g.M4_2)
        # print("M4_2  ", ss3)
        # ss4 = motif_num(G, g.M4_3)
        # print("M4_3  ", ss4)
        # ss5 = motif_num(G, g.M4_4)
        # print("M4_4  ", ss5)
        for i in range(3,7):
            result.append(motif_num(G, g.MO[i]))
        return result

    if k==5:
        # ss6 = motif_num(G, g.M5_1)
        # print("M5_1  ", ss6)
        # ss7 = motif_num(G, g.M5_2)
        # print("M5_2  ", ss7)
        # ss8 = motif_num(G, g.M5_3)
        # print("M5_3  ", ss8)
        # ss9 = motif_num(G, g.M5_4)
        # print("M5_4  ", ss9)
        # ss10 = motif_num(G, g.M5_5)
        # print("M5_5  ", ss10)
        # ss11 = motif_num(G, g.M5_6)
        # print("M5_6  ", ss11)
        # ss12 = motif_num(G, g.M5_7)
        # print("M5_7  ", ss12)
        # ss13 = motif_num(G, g.M5_8)
        # print("M5_8  ", ss13)
        # ss14 = motif_num(G, g.M5_9)
        # print("M5_9  ", ss14)
        for i in range(7,15):
            result.append(motif_num(G, g.MO[i]))
        return result
    if k==6:
        # ss6 = motif_num(G, g.M6_1)
        # print("M6_1  ", ss6)
        # ss7 = motif_num(G, g.M6_2)
        # print("M6_2  ", ss7)
        # ss8 = motif_num(G, g.M6_3)
        # print("M6_3  ", ss8)
        # ss9 = motif_num(G, g.M6_4)
        # print("M6_4  ", ss9)
        # ss10 = motif_num(G, g.M6_5)
        # print("M6_5  ", ss10)
        # ss11 = motif_num(G, g.M6_6)
        # print("M6_6  ", ss11)
        # ss12 = motif_num(G, g.M6_7)
        # print("M6_7  ", ss12)
        # ss13 = motif_num(G, g.M6_8)
        # print("M6_8  ", ss13)
        # ss14 = motif_num(G, g.M6_9)
        # print("M6_9  ", ss14)
        # ss6 = motif_num(G, g.M6_10)
        # print("M6_10  ", ss6)
        # ss6 = motif_num(G, g.M6_11)
        # print("M6_11  ", ss6)
        # ss7 = motif_num(G, g.M6_12)
        # print("M6_12  ", ss7)
        # ss8 = motif_num(G, g.M6_13)
        # print("M6_13  ", ss8)
        # ss9 = motif_num(G, g.M6_14)
        # print("M6_14  ", ss9)
        # ss10 = motif_num(G, g.M6_15)
        # print("M6_15  ", ss10)
        # ss11 = motif_num(G, g.M6_16)
        # print("M6_16  ", ss11)
        # ss12 = motif_num(G, g.M6_17)
        # print("M6_17  ", ss12)
        # ss13 = motif_num(G, g.M6_18)
        # print("M6_18  ", ss13)
        # ss14 = motif_num(G, g.M6_19)
        # print("M6_19  ", ss14)
        # ss6 = motif_num(G, g.M6_20)
        # print("M6_20  ", ss6)
        for i in range(15,35):
            result.append(motif_num(G, g.MO[i]))
        return result

if __name__ ==  "__main__":
    # G=nx.read_edgelist("mydata/test2.txt", create_using=nx.DiGraph())
    import pandas as pd
    data = pd.read_csv("mydata/politifact279.txt", sep=" ", names=["a", "b", "w"])
    G = nx.from_pandas_edgelist(data, source="a", target="b", create_using=nx.DiGraph())

    print("node num  ",len(G.nodes))
    print("edge num  ",len(G.edges))

    a=K_motif_num(G,6)#K阶模体数
    for i in a:
        print(i)

    g=motif()#模体类，里面封装了3-6节点传播模体，（树状无环）
    a=motif_num(G, g.M4_2)#一种模体数
    print(a)

    t1 = time.time()
    a=all_motif_num(G)  # 所有种类模体数
    for i in a:
        print(i)
    t2 = time.time()
    print("time1  ", t2 - t1)
    print("_______________________________")
    a = all_motif_num2(G)  # 所有种类模体数,一次性算所有的模体，通过模体的拼接，速度更快。
    for i in a:
        print(i)
    t3=time.time()
    print("time2  ",t3-t2)




