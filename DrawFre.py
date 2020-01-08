
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import mathModule as mymath
import DataPro as mydp




def myTest():
    path1 = "huawei\\fre2M.txt"
    dic1 = mydp.readFre(path1)
    path2 = "huawei\\fre4M.txt"
    dic2 = mydp.readFre(path2)
    con = mymath.conDifCo(dic1, dic2)
    dic1, dic2 = mymath.xLablePro(dic1, dic2)
    mydp.probabilitySuperposition(dic1)
    mydp.probabilitySuperposition(dic2)
    mydp.probabilitySuperposition(con)
    #dic4 = mymath.mytest()
   # mydp.probabilitySuperposition(dic4)
    plt.plot(list(con.keys()), list(con.values()))
    plt.plot(list(dic1.keys()), list(dic1.values()))
    plt.plot(list(dic2.keys()), list(dic2.values()))
   # plt.plot(list(dic4.keys()), list(dic4.values()))
    plt.ylabel('frequency')
    plt.show()



def drawPiTest():
    path1="huawei\\pi_8M.txt"
    data1 = mydp.readSingleDate(path1, 0, 30)
    path2 = "tencent\\pi_8M.txt"
    data2 = mydp.readSingleDate(path2, 0, 30)
    path3 = "ali\\pi_8M.txt"
    data3 = mydp.readSingleDate(path3, 0, 30)
    plt.plot(data2,color='red', label="TX",linestyle='--',marker='o')
    plt.plot(data1, color='blue', label="HW",linestyle='--',marker='>')
    plt.plot(data3, color='black', label="Ali", linestyle='--', marker='*')
    plt.ylabel('value')
    plt.show()
drawPiTest()

