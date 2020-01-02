import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import DataPro as mydp
from queue import Queue

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


class DagAssistant():
    #dag is a 2-D array,tasknum from 0
    def isEnd(tasknum, dag):
        flag = True
        for j in range(0, len(dag)):
            if (dag[tasknum][j] == 1):
                flag = False
        if (flag == True):
            return True
        return False
def mytest():
    dag=[]
   dagA=DagAssistant()


