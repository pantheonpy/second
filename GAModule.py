import random as ra
import Code.DAGAssistant as DGtool

def crossFun(individualX,individualY,dag):
    taskNum=len(dag)
    point = ra.randint(1, taskNum - 1)
    v1 = individualX[0][0:point]
    v2 = individualY[0][0:point]
    for i in range(0, taskNum):
        if (individualY[0][i] not in v1):
            v1.append(individualY[0][i])
    for i in range(0, taskNum):
        if (individualX[0][i] not in v2):
            v2.append(individualX[0][i])
    individualX[0]=v2
    individualY[0]=v1
    for j in range(0, point + 1):

        v = individualX[2][j]
        tp1 = individualX[1][v - 1]
        tp2 = individualY[1][v - 1]
        tempX = []
        tempY = []
        for i in range(point + 1, taskNum):
            if (individualX[2][i] == v):
                tempX.append(1)
        for i in range(point, taskNum):
            if (individualY[2][i] == v):
                tempY.append(1)
        vinX = len(tempX)
        vinY = len(tempY)
        if (tp1 != tp2):
            if (vinX > vinY):
                individualY[1][v - 1] = tp1
            else:
                individualX[1][v - 1] = tp2
        v = individualY[2][j]
        tp1 = individualY[1][v - 1]
        tp2 = individualX[1][v - 1]
        tempX = []
        tempY = []
        for i in range(point, taskNum):
            if (individualX[2][i] == v):
                tempX.append(1)
        for i in range(point, taskNum):
            if (individualY[2][i] == v):
                tempY.append(1)
        vinX = len(tempX)
        vinY = len(tempY)
        if (tp1 != tp2):
            if (vinY > vinX):
                individualX[1][v - 1] = tp1
            else:
                individualY[1][v - 1] = tp2
        temp1 = individualX[2][j]
        temp2 = individualY[2][j]
        individualX[2][j] = temp2
        individualY[2][j] = temp1
        return individualX,individualY

def gaIniFun(dag,typeNum,perTypeNum,taskNum):#perNum is the number of per Type VM
    mark=[0 for i in range(taskNum)]
    taskVM = [0 for i in range(taskNum)]
    vmType = [0 for i in range(taskNum)]
    taskIndex = [0 for i in range(taskNum)]
    cixu = 1
    while (True):
        a = ra.randint(0, taskNum - 1)
        if (mark[a] == 1):
            continue
        Parents = DGtool.getParents(a, dag)
        flag = True
        for i in Parents:
            if (mark[i] == 0):
                flag = False
        if (flag == True):
            taskIndex[cixu - 1] = a
            mark[a] = 1
            cixu = cixu + 1
        if (cixu == taskNum + 1):
            break
    for i in range(0, taskNum):
        taskVM[i] = ra.randint(1, perTypeNum)
        vmType[i] = ra.randint(1, typeNum)
    return [taskIndex, vmType, taskVM]

def mutationFun(individual,dag):
    taskNum=len(dag)
    point = ra.randint(1, taskNum - 1)
    cout = 0
    for i in range(0, taskNum):
        if (DGtool.isCanArrvie(dag, min(i, point), max(i, point)) == False):
            cout = cout + 1
    cout = min(0, cout - 1)
    if (cout > 0):
        select = ra.randint(1, cout - 1)
        for i in range(0, taskNum):
            if (DGtool.isCanArrvie(dag, min(i, point), max(i, point)) == False):
                if (select == 1):
                    temp = individual[0][point]
                    individual[0][point] = individual[0][i]
                    individual[0][i] = temp
                else:
                    select = select - 1


def fitnessFun(individual,avePerf, unitPrice,deadLine,dag,taskTypeArray):
    #avePerf is a array=[[ave time of super_pi2M in type 1,4M,8M],[ave time of super_pi2M in type 2,4M,8M],[]]
    everyTaskTimes = [0 for i in range(len(dag))]
    everyTaskCosts = [0 for i in range(len(dag))]
    for i in range(0, len(dag)):
        j=individual[0][i]
        #j=taskID
        taskType=taskTypeArray[j]
        vmType=individual[0][j]
        aveTime=avePerf[vmType-1][taskType]
        aveCost=aveTime*unitPrice[vmType]
        everyTaskTimes[j]=maxFinishTimeofParentFun(dag,everyTaskTimes,j,individual)+aveTime
        everyTaskCosts[j]= aveCost
    diffrentVM=DGtool.aryyNotSame(individual[1],individual[2])
    totalcost = 0
    transDelay=1
    for vm in diffrentVM:
        totalcost=totalcost+1*unitPrice[vm[0]-1]
    for icost in everyTaskCosts[j]:
        totalcost=totalcost+icost
    D=max(everyTaskTimes)
    score=-totalcost
    if (D > deadLine):
        score= score*1.05
    return score,max(everyTaskTimes),totalcost

def maxFinishTimeofParentFun(dag,cTime,taskID,individual):
    Parents = DGtool.getParents(taskID, dag)
    everyTaskTimes=[]
    if(len(Parents)<1):
        return 0
    else:
        for i in Parents:
            if(individual[1][i]==individual[1][taskID] and individual[2][i]==individual[2][taskID]):
                finishTime=cTime[i]
                everyTaskTimes.append(finishTime)
            else:
                finishTime=cTime[i]+0.1
                everyTaskTimes.append(finishTime)
    return max(everyTaskTimes)

def selectGroupFun(group,limit,avePerf,unitPrice,deadLine,dag,taskTypeArray):
    newGroup = []
    temp = []
    for i in range(0,len(group)):
        score,makeSpan,cost = fitnessFun(group[i],avePerf,unitPrice,deadLine,dag,taskTypeArray)
        temp.append([score,i])
    for j in range(0,len(temp)):
        for i in range(0,len(temp)):
            if(temp[j][0]>temp[i][0]):
                tv=temp[j]
                temp[j] = temp[i]
                temp[i]=tv
    for i in range(0,limit):
        newGroup.append(group[temp[i][1]])
    return newGroup

def mainGAFun(dag,typeNum,perTypeNum,Iter,iniNumIndividual,avePerf,unitPrice,deadLine,taskTypeArray):
    #individual is a 2-D array  [[task],[vmType],[vnNumber]]
    #Group is a array [individual]
    Group=[]
    for i in range(0,iniNumIndividual):
        tempIndividual=gaIniFun(dag,typeNum,perTypeNum)
        Group.append(tempIndividual)
    for i in range(0,Iter):
        print("迭代次数",i)
        tempGroup=[]
        for index in range(0,len(Group)):
            individualX=Group[index]
            indey=ra.randint(1,len(Group)-1)
            if(indey==index):
                indey=index-1
            individualY=Group[indey]
            crossFun(individualX, individualY,dag)
            tempGroup.append(individualX)
            tempGroup.append(individualY)
            pm=ra.randint(0,10)
            if(pm==2):
                mutationFun(individualY,dag)
        Group=selectGroupFun(tempGroup,int((1+len(tempGroup))/2),avePerf,unitPrice,deadLine,dag,taskTypeArray)
    Group=selectGroupFun(Group,4)
    return Group

u
