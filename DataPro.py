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

def readInitialFile(path,startnum,totalnum):#Relative path /superpi/**,startnum=81*len,totalnum=lenth(superpi_2M)
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

# path="tencent\\data.txt"
# writePath="tencent\\"
# MainFreFun(path,writePath,0,250)
# MainSingleData(path,writePath,0,250)


