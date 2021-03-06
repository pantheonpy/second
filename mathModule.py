import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import DataPro as mydp
from queue import Queue
import random as ra
import os
from xml.dom.minidom import parse
import xml.dom.minidom



def getXMLtoDag(filePath,taskCount):
    totalpath = os.getcwd() + "\\data\\"+filePath
    DAG = np.zeros((taskCount, taskCount), dtype=int)
    transTime = np.zeros((taskCount, taskCount))
    xmlFile=totalpath
    DOMTree = xml.dom.minidom.parse(xmlFile)
    collection = DOMTree.documentElement
    childrens = collection.getElementsByTagName("child")

    for child in childrens:
        child_id = child.getAttribute('ref')
        child_id = int(child_id[2:]) - 1
        # print('Child: ', child_id)
        parents = child.getElementsByTagName('parent')
        for parent in parents:
            parent_id = parent.getAttribute('ref')
            parent_id = int(parent_id[2:]) - 1
            ttime = float(parent.getAttribute('TTime'))
            # print(parent_id,ttime)
            DAG[parent_id, child_id] = 1
            transTime[parent_id, child_id] = ttime
    return DAG, transTime

def getEnrty(dag):
    entrys=[]
    for i in range(0,len(dag)):
        flag=True
        for j in range(0,len(dag)):
            if(dag[j][i]==1):
                flag=False
        if(flag==True):
            entrys.append(i)
    return entrys

def isEnd(tasknum,dag):
    flag=True
    for j in range(0, len(dag)):
        if (dag[tasknum][j] == 1):
            flag=False
    if(flag==True):
        return True
    return False

def getParents(tasknow,dag):
    parents=[]
    for i in range(0,len(dag)):
        if(dag[i][tasknow]==1):
            parents.append(i)
    return parents

def getChildren(tasknow,dag):
    Children=[]
    for i in range(0,len(dag)):
        if(dag[tasknow][i]==1):
            Children.append(i)
    return Children

def getCPave(dag,tasknow,tasktypeArr):
    tasksize=[]
    for i in range(len(dag)):
        taskType=tasktypeArr[i]
        if (taskType == 1):
            tasksize.append(4)
        if (taskType == 2):
            tasksize.append(9)
        if (taskType == 3):
            tasksize.append(20)
    size,path=diguiCP(tasknow,dag,tasksize)
    path.reverse()
    return path

def diguiCP(taskNow,dag,taskSizeArr):
    if(isEnd(taskNow,dag=dag)):
        CP = []
        CP.append(taskNow)
        return taskSizeArr[taskNow],CP
    else:
        children=getChildren(taskNow,dag)
        temps=0
        tempc=[]
        for i in children:
            tempSize,tempCP=diguiCP(i,dag,taskSizeArr)
            if(tempSize>temps):
                temps=tempSize
                tempc=tempCP
        path=tempc.copy()
        path.append(taskNow)
        return temps+taskSizeArr[taskNow],path

# def getCriPath(dag,tasknow,tasksize):#路径的任务规模最大
#     CP=[tasknow]
#     now=tasknow
#     while(True):
#         if (isEnd(now, dag)):
#             break
#
#         temp=0
#         numtask=0
#         for j in range(0,len(dag)):
#             if(dag[now][j]==1):
#                 if(tasksize[j]>temp):
#                     temp=tasksize[j]
#                     numtask=j
#         now=numtask
#         CP.append(numtask)
#     return  CP

def isCanArrvie(dag,start,end):
    if(start==end):
        return False
    q=Queue()
    q.put(start)
    flag = False
    while(q.qsize()!=0):
        p=q.get()
        for i in range(0, len(dag)):
            if (dag[p][i] == 1):
                q.put(i)
                if(i==end):
                    return True
    return False

def aryyNotSame(X,Y):
    diffrent=[[X[0],Y[0]]]
    for i in range(1,len(X)):
        for dar in diffrent:
            if(X[i]!=dar[0] or Y[i]!=dar[1]):
                diffrent.append([X[i],Y[i]])
                break
    return diffrent

def conDifCo(oDic1,oDic2):#Convolution of different coordinates,oDic={x1:y1...xn:yn}
    oDic1,oDic2=xLablePro(oDic1,oDic2)
    y1=list(oDic1.values())
    y2 = list(oDic2.values())
    y3=scipy.signal.convolve(y1,y2)
    x1=list(oDic1.keys())
    temp_start=2*x1[0]
    x3=[]
    for i in range(0,len(y3)):
        x3.append(round(temp_start+i*0.1,1))
    newDic={}
    for i in range(0,len(x3)):
        newDic[x3[i]]=round(y3[i],8)
    return newDic

def xLablePro(oDic1,oDic2):
    #Before convolution, the abscissa should be treated uniformly
    #X coordinate equal processing,Coordinate interval can only be 0.1s
    # There must be only one decimal place,otherwise the precision is lost
    x1_start = list(oDic1.keys())[0]
    x2_start = list(oDic2.keys())[0]
    x1_end = list(oDic1.keys())[-1]
    x2_end = list(oDic2.keys())[-1]
    x_newStart = min(x1_start, x2_start)
    x_newEnd = max(x2_end, x1_end)
    interval = 0.1# 0.1sec times=10
    times=10
    intervalNum = int((x_newEnd*10 - x_newStart*10) )
    for i in range(0, intervalNum+1):
        tempKey = round(x_newStart + i * 0.1, 1)
        if (tempKey not in oDic1):
            oDic1[tempKey] = 0
        if (tempKey not in oDic2):
            oDic2[tempKey] = 0
    oDic1 = mydp.sortDic(oDic1)
    oDic2 = mydp.sortDic(oDic2)
    return oDic1,oDic2





def fakeDate():
    ten2=4.2
    ten2a=[]
    ten4=9.0
    ten4a = []
    ten8=20.1
    ten8a = []
    ali2=5.65
    ali2a=[]
    ali4=12.4
    ali4a = []
    ali8=26.985
    ali8a = []
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ten2,1)
        ten2+=0.005
        ten2a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ten4,1)
        ten4 += 0.01
        ten4a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ten8,1)
        ten8+=0.02
        ten8a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ali2,1)
        ali2-=0.003
        ali2a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ali4,1)
        ali4 -= 0.006
        ali4a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ali8,1)
        ali8 -= 0.012
        ali8a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ten2,1)
        ten2 -= 0.003
        ten2a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ten4,1)
        ten4 -= 0.006
        ten4a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ten8,1)
        ten8 -= 0.012
        ten8a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ali2,1)
        ali2+=0.002
        ali2a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.02)
        temp=round(p*ali4,1)
        ali4 += 0.005
        ali4a.append(temp)
    for i in range(150):
        p=ra.uniform(0.98,1.01)
        temp=round(p*ali8,1)
        ali8 += 0.01
        ali8a.append(temp)

    totalpath = os.getcwd() + "\\data\\superpi\\tencent\\pi_2M.txt"
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for i in ten2a:
        value = str(i)
        f.write(value + '\n')
    f.close()

    totalpath = os.getcwd() + "\\data\\superpi\\tencent\\pi_4M.txt"
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for i in ten4a:
        value = str(i)
        f.write(value + '\n')
    f.close()

    totalpath = os.getcwd() + "\\data\\superpi\\tencent\\pi_8M.txt"
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for i in ten8a:
        value = str(i)
        f.write(value + '\n')
    f.close()

    totalpath = os.getcwd() + "\\data\\superpi\\ali\\pi_2M.txt"
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for i in ali2a:
        value = str(i)
        f.write(value + '\n')
    f.close()

    totalpath = os.getcwd() + "\\data\\superpi\\ali\\pi_4M.txt"
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for i in ali4a:
        value = str(i)
        f.write(value + '\n')
    f.close()

    totalpath = os.getcwd() + "\\data\\superpi\\ali\\pi_8M.txt"
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for i in ali8a:
        value = str(i)
        f.write(value + '\n')
    f.close()





#fakeDate()


# def test():
#     dag=[[0,1,1,1,0,0,0],
#          [0,0,0,0,1,0,0],
#          [0,0,0,0,0,1,0],
#          [0,0,0,0,0,0,1],
#          [0,0,0,0,0,0,1],
#          [0,0,0,0,0,0,1],
#          [0,0,0,0,0,0,0]]
#     tasksizeA=[1,1,1,3,1,1,3]
#     y=getCPave(dag,0,tasksizeA)
#     print(y)
# test()

