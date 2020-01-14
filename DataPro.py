import os
import re
def frequencyCount(t):#t is a array
    #return dic
    d = dict()  ###空字典
    lenth=len(t)
    for i in t:#i is key
        i=round(i,1)
        if i not in d:
            d[i] = 1
        else:
            d[i] += 1
    for i in d:
        d[i]=round(d[i]/lenth,8)
    return d

def readInitialFile(path,startnum,totalnum):
    #Relative path /superpi/**,startnum=81*len,totalnum=lenth(superpi_2M)
    #return arrary1,arrar2,arrar3  ;arrar is a set of execute time of 2m,4m,8m
    totalpath=os.getcwd()+"\\data\\superpi\\"+path
    superpi_2M=[]
    superpi_4M = []
    superpi_8M = []
    flag=0
    for line in open(totalpath):
        flag+=1
        if(flag%81==26 and flag>=startnum*81):
            temp = re.findall(r'-?\d+\.?\d*e?-?\d*?', line)[0] if re.findall(r'-?\d+\.?\d*e?-?\d*?', line)[
                                                                      0] != "" else ""

            superpi_2M.append(temp)
        if (flag % 81 == 53 and flag>=startnum*81):
            temp = re.findall(r'-?\d+\.?\d*e?-?\d*?', line)[0] if re.findall(r'-?\d+\.?\d*e?-?\d*?', line)[
                                                                      0] != "" else ""
            superpi_4M.append(temp)
        if (flag % 81 == 0 and flag>=startnum*81):
            temp = re.findall(r'-?\d+\.?\d*e?-?\d*?', line)[0] if re.findall(r'-?\d+\.?\d*e?-?\d*?', line)[
                                                                  0] != "" else ""
            superpi_8M.append(temp)
        if(len(superpi_2M)==totalnum and len(superpi_4M)==totalnum and len(superpi_8M)==totalnum):
            break
    return superpi_2M,superpi_4M,superpi_8M

def characterArrayProcessingRoud(arryString,roundNum):#to round 1 float
    arryFloat=[]
    for i in arryString:
        num1=float(i)
        num1=round(num1,roundNum)#
        arryFloat.append(num1)
    return arryFloat



def MainFreFun(path,writePath,startNum,totalNum):#Data path to be processed，Relative path /superpi/**
    superpi_2M, superpi_4M, superpi_8M=readInitialFile(path,startNum,totalNum)
    arryFloat_2M=characterArrayProcessingRoud(superpi_2M,1)
    arryFloat_4M = characterArrayProcessingRoud(superpi_4M,1)
    arryFloat_8M = characterArrayProcessingRoud(superpi_8M,1)
    fre2M = frequencyCount(arryFloat_2M)
    fre4M = frequencyCount(arryFloat_4M)
    fre8M = frequencyCount(arryFloat_8M)
    fre2M=sortDic(fre2M)
    fre4M=sortDic(fre4M)
    fre8M=sortDic(fre8M)
    fre2M=xLableprocessing(fre2M)
    fre4M=xLableprocessing(fre4M)
    fre8M=xLableprocessing(fre8M)
    writeFreDate(fre2M,writePath,"fre2M.txt")
    writeFreDate(fre4M, writePath, "fre4M.txt")
    writeFreDate(fre8M, writePath, "fre8M.txt")


def writeFreDate(data,writePath,filename):#data is dic
    totalpath = os.getcwd() + "\\data\\superpi\\" + writePath+"\\"+filename
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for k, v in data.items():
        value = str(v)
        key=str(k)
        f.write(key + '\n')
        f.write(value + '\n')
    f.close()

def writeSingleDate(data,writePath,filename):#data is array
    totalpath = os.getcwd() + "\\data\\superpi\\" + writePath + "\\" + filename
    path = totalpath
    f = open(path, 'w', encoding='utf-8')
    for i in data:
        value = str(i)
        f.write(value + '\n')
    f.close()


def sortDic(orDic):
    #return dic
    arryKey=[]
    for k, v in orDic.items():
        key = round(float(k),1)
        arryKey.append(key)
    arryKey=sorted(arryKey)
    arrayValue=[0 for i in range(len(arryKey))]
    newDic=dict(zip(arryKey,arrayValue))
    for i in newDic:
        newDic[i]=orDic[i]
    return newDic

def xLableprocessing(oDic):#Raw data PDF dictionary to Equidistant dictionary
    #return dic
    keyArray=list(oDic.keys())
    dataStartIndex=keyArray[0]
    dataEndIndex=keyArray[len(keyArray)-1]
    interval=0.1
    intervalNum=int( (dataEndIndex-dataStartIndex) * (1/interval) )
    for i in  range (0,intervalNum+1):
        tempKey=round(keyArray[0]+i*0.1,1)
        if(tempKey not in oDic):
            oDic[tempKey]=0
    oDic=sortDic(oDic)
    return oDic

def probabilitySuperposition(oDic):
    #return dic
    valueArray=list(oDic.values())
    keyArray = list(oDic.keys())
    for i in range(0,len(keyArray)):
        temp=0
        for j in range(0,i+1):
            temp=temp+valueArray[j]
        oDic[keyArray[i]]=round(temp,8)
    return oDic


def MainSingleData(path,writePath,startNum,totalNum):
    superpi_2M, superpi_4M, superpi_8M = readInitialFile(path, startNum, totalNum)
    arryFloat_2M = characterArrayProcessingRoud(superpi_2M,1)
    arryFloat_4M = characterArrayProcessingRoud(superpi_4M,1)
    arryFloat_8M = characterArrayProcessingRoud(superpi_8M,1)
    writeSingleDate(arryFloat_2M,writePath,"pi_2M.txt")
    writeSingleDate(arryFloat_4M,writePath,"pi_4M.txt")
    writeSingleDate(arryFloat_8M,writePath,"pi_8M.txt")


def readSingleDate(path,startNum,totalNum):#include filename,Relative path /superpi/**,totalNum=len(data)
    #return array
    totalpath = os.getcwd() + "\\data\\superpi\\" + path
    data=[]
    flag = 0
    for line in open(totalpath):
        flag += 1
        if(flag>=startNum):
            data.append(float(line))
        if (len(data) == totalNum):
            break
    return data

def readFre(path):#include filename ,Relative path /superpi/**
    #Return dic
    totalpath = os.getcwd() + "\\data\\superpi\\" + path
    arrayKey=[]
    arrayValue=[]
    roudKeyNum=1
    roudValueNum=8
    index=0
    for line in open(totalpath):
        index += 1
        if(index%2==1):
            temp=round(float(line),roudKeyNum)
            arrayKey.append(temp)
        if (index % 2 == 0):
            temp = round(float(line), roudValueNum)
            arrayValue.append(temp)
    newDic={}
    for i in range(0, len(arrayKey)):
        newDic[arrayKey[i]] = arrayValue[i]
    return newDic


def dataProTest():
    path="huawei\\hwdata.txt"
    writePath="huawei\\"
    MainFreFun(path,writePath,0,250)
    MainSingleData(path,writePath,0,250)

def getAVE(filename):
    #hua 2M-4.035  4M-8.9  8M-19.47          0.1526    0.5
    #tencet  2M-4.20  4M-9.02 8M-20.29       0.36      0.4
    #ali    2M-5.565   4m-12.398 8M-26.985    0.242    0.25
    py=readSingleDate(filename,0,250)
    total=0
    for i in py:
        total=total+i
    return total/len(py)

def getVMDATAS():
    aveALI2M=getAVE("ali\\pi_2M.txt")
    aveALI4M = getAVE("ali\\pi_4M.txt")
    aveALI8M = getAVE("ali\\pi_8M.txt")
    aveTX2M=getAVE("tencent\\pi_2M.txt")
    aveTX4M = getAVE("tencent\\pi_4M.txt")
    aveTX8M = getAVE("tencent\\pi_8M.txt")
    aveHW2M=getAVE("huawei\\pi_2M.txt")
    aveHW4M = getAVE("huawei\\pi_4M.txt")
    aveHW8M = getAVE("huawei\\pi_8M.txt")
    allALI2M=readSingleDate("ali\\pi_2M.txt",0,240)
    allALI4M = readSingleDate("ali\\pi_4M.txt", 0, 240)
    allALI8M = readSingleDate("ali\\pi_8M.txt", 0, 240)
    allTX2M=readSingleDate("tencent\\pi_2M.txt", 0, 240)
    allTX4M = readSingleDate("tencent\\pi_4M.txt", 0, 240)
    allTX8M = readSingleDate("tencent\\pi_8M.txt", 0, 240)
    allHW2M=readSingleDate("huawei\\pi_2M.txt", 0, 240)
    allHW4M = readSingleDate("huawei\\pi_4M.txt", 0, 240)
    allHW8M = readSingleDate("huawei\\pi_8M.txt", 0, 240)
    freHW2M=readFre("huawei\\fre2M.txt")
    freHW4M = readFre("huawei\\fre4M.txt")
    freHW8M = readFre("huawei\\fre8M.txt")
    freAli2M=readFre("ali\\fre2M.txt")
    freAli4M = readFre("ali\\fre4M.txt")
    freAli8M = readFre("ali\\fre8M.txt")
    freTX2M=readFre("tencent\\fre2M.txt")
    freTX4M = readFre("tencent\\fre4M.txt")
    freTX8M = readFre("tencent\\fre8M.txt")
    VMDATA=[]
    huawei={"pi2M":allHW2M,"pi4M":allHW4M,"pi8M":allHW8M,"avepi2M":aveHW2M,
            "avepi4M":aveHW4M,"avepi8M":aveHW8M,"price":0.5,"fre2M":freHW2M,"fre4M":freHW4M,"fre8M":freHW8M}

    tenxun = {"pi2M": allTX2M, "pi4M": allTX4M, "pi8M": allTX8M, "avepi2M": aveTX2M, "avepi4M": aveTX4M,
              "avepi8M": aveTX8M, "price": 0.4,"fre2M":freTX2M,"fre4M":freTX4M,"fre8M":freTX8M}
    ali = {"pi2M": allALI2M, "pi4M": allALI4M, "pi8M": allALI8M, "avepi2M": aveALI2M, "avepi4M": aveALI4M,
              "avepi8M": aveALI8M, "price": 0.25,"fre2M":freAli2M,"fre4M":freAli4M,"fre8M":freAli8M}
    VMDATA=[huawei,tenxun,ali]
    return VMDATA

def doFre():
    path2="ali\\pi_2M.txt"
    path4 = "ali\\pi_4M.txt"
    path8 = "ali\\pi_8M.txt"
    pi2M=readSingleDate(path2,0,250)
    pi4M = readSingleDate(path4, 0, 250)
    pi8M = readSingleDate(path8, 0, 250)
    arryFloat_2M = characterArrayProcessingRoud(pi2M, 1)
    arryFloat_4M = characterArrayProcessingRoud(pi4M, 1)
    arryFloat_8M = characterArrayProcessingRoud(pi8M, 1)
    fre2M = frequencyCount(arryFloat_2M)
    fre4M = frequencyCount(arryFloat_4M)
    fre8M = frequencyCount(arryFloat_8M)
    fre2M = sortDic(fre2M)
    fre4M = sortDic(fre4M)
    fre8M = sortDic(fre8M)
    fre2M = xLableprocessing(fre2M)
    fre4M = xLableprocessing(fre4M)
    fre8M = xLableprocessing(fre8M)
    writePath="ali\\"
    writeFreDate(fre2M, writePath, "fre2M.txt")
    writeFreDate(fre4M, writePath, "fre4M.txt")
    writeFreDate(fre8M, writePath, "fre8M.txt")

#doFre()
