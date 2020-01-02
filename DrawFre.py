
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import mathModule as mymath
import DataPro as mydp




def myTest():
    path1 = "tencent\\fre2M.txt"
    dic1 = mydp.readFre(path1)
    path2 = "tencent\\fre4M.txt"
    dic2 = mydp.readFre(path2)
    con = mymath.conDifCo(dic1, dic2)
    dic1, dic2 = mymath.xLablePro(dic1, dic2)
    mydp.probabilitySuperposition(dic1)
    mydp.probabilitySuperposition(dic2)
    mydp.probabilitySuperposition(con)
    dic4 = mymath.mytest()
    mydp.probabilitySuperposition(dic4)
    plt.plot(list(con.keys()), list(con.values()))
    plt.plot(list(dic1.keys()), list(dic1.values()))
    plt.plot(list(dic2.keys()), list(dic2.values()))
    plt.plot(list(dic4.keys()), list(dic4.values()))
    plt.ylabel('frequency')
    plt.show()




