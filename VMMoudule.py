from scipy import integrate
import mathModule as myMathTool



class VmInstance(object):
    def __init__(self):
        self.instanceID=-1  #The ID of virtual machine instances
        self.vmType=-1      #The type of virtual machine instances
        self.taskTimeGroup=[]  #Time intervals for different tasks such as [4.5,8.9] means  running time is 8.9-4.5
        self.exIdeleTime = -1    #Estimated free time that all tasks on the virtual machine will been completed
        self.realIdeleTime = -1  #Actual free time,All tasks on the virtual machine have been completed
        self.isAvailable=True   #Is the virtual machine released? False is not avalable
        self.createDelay=0    #Startup delay for creating virtual machines
        self.vmType=-1        #start from 1
        self.VMDATA=[]



    def getCost(self):
        for i in self.taskTimeGroup:
            time=i[1]-i[0]+time
        cost=time*self.VMDATA["price"]
        #print(self.vmType,self.price,":",time,cost)
        return cost


    def appendTaskTimeGroup(self,rStarttime,rEndtime):
        self.taskTimeGroup.append([rStarttime,rEndtime])


    def createNewVM(self,vmtype,preStartTime,VMDATAS):
        self.VMDATA=VMDATAS[vmtype-1]
        self.vmType = vmtype
        self.exIdeleTime =preStartTime
        self.realIdeleTime=preStartTime



    def taskRealRunTime(self,startTime,taskType):
        startIndex = int(startTime/60)
        Runtime = 0
        if (taskType == 1):
            preRuntime = self.VMDATA["pi2M"][startIndex]
        if (taskType == 2):
            preRuntime = self.VMDATA["pi4M"][startIndex]
        if (taskType == 3):
            preRuntime = self.VMDATA["pi8M"][startIndex]
        Runtime=preRuntime
        return Runtime

    def taskRunTimeWithAve(self,taskType):
        preRuntime=0
        if(taskType==1):
            preRuntime=self.VMDATA["avepi2M"]
        if (taskType == 2):
            preRuntime = self.VMDATA["avepi4M"]
        if (taskType == 3):
            preRuntime = self.VMDATA["avepi8M"]
        return preRuntime

    def pathRunTimeWithAve(self,taskTypeArr,TaskSet):
        time=0
        for taskid in TaskSet:
            if (taskTypeArr[taskid] == 1):
                time += self.VMDATA["avepi2M"]
            if (taskTypeArr[taskid] == 2):
                time +=self.VMDATA["avepi4M"]
            if (taskTypeArr[taskid] == 3):
                time += self.VMDATA["avepi8M"]
        return time






    #对执行任务，进行模拟，
    # 参数taskTimeArr[预计，实际]父节点结果传输过来的预计，实际时间
    # 参数VMDATAS：虚拟机数据集
    def runTask(self,taskDetails,taskTimeArr):#使用AR估计任务完成时间
        taskDetails.vmInsID = self.instanceID
        taskDetails.preStartTime=max(taskTimeArr[0],self.exIdeleTime)#任务的预计开始时间
        taskDetails.reaStartTime=max(taskTimeArr[1],self.realIdeleTime)#任务的实际开始时间
        #因为模拟运行，执行时间
        rRunTime=self.taskRealRunTime(taskDetails.reaStartTime,taskDetails.taskType)
        #算预计执行时间，任务开始后才能估算预计结束时间
        pRunTime=self.taskRunTimeWithAve(taskDetails.taskType)
        taskDetails.reaEndTime = taskDetails.reaStartTime + rRunTime
        taskDetails.preEndTime = taskDetails.reaStartTime + pRunTime
        self.exIdeleTime = taskDetails.preEndTime
        self.realIdeleTime = taskDetails.reaEndTime
        self.appendTaskTimeGroup(taskDetails.reaStartTime,taskDetails.reaEndTime)

    def print(self):
        print("instance:", self.instanceID," Type:", self.vmType,
            "时间组：",self.taskTimeGroup)


class VmPool():
    def __init__(self):
        self.vmList = []  #List of VmInstance
    def getVmInstanceByID(self,id):
        for i in range(0,len(self.vmList)):
            if(self.vmList[i].instanceID==id):
                return self.vmList[i]
        return False
    def appendVmInstance(self,vmInstance):
        self.vmList.append(vmInstance)
        vmInstance.instanceID=len(self.vmList)
    def totalCost(self):
        totalCost=0
        for i in range(0,len(self.vmList)):
            totalCost=totalCost+self.vmList[i].getCost()
        return totalCost

    def totalMS(self):
        maxT=0
        minT=float("inf")
        for i in range(0, len(self.vmList)):
            if(self.vmList[i].taskTimeGroup[1]>=maxT):
                maxT=self.vmList[i].taskTimeGroup[1]
            if(self.vmList[i].taskTimeGroup[0]<=minT):
                minT=self.vmList[i].taskTimeGroup[0]
        return maxT-minT





class TaskDetails():
    def __init__(self, taskid,taskType):
        self.taskID = taskid
        self.taskType=taskType
        self.vmInsID = -1      #Virtual Machine Instances for Task Assignment
        self.preStartTime = -1 # Task estimated start time is obtained according to different algorithms
        self.reaStartTime = -1 #The actual time a task can start executing depends on the completion time of the parent node,
        # transmission delay, virtual machine availability time.
        self.preEndTime = -1   #The expected completion time ，depends on the expected start time and estimated performance.
        self.reaEndTime = -1   #Actual completion time

    def print(self):
        print("任务：",self.taskID,"虚拟机:",self.vmInsID," 预开:",self.preStartTime," 实开:",self.reaStartTime," 预结:",self.preEndTime," 实结:",self.reaEndTime)



class TaskListAssistant():#Contains details of task execution
    def __init__(self,dag,transTime):
        self.taskDetailsList=[] #Details of each workflow task
        self.dag = dag
        self.transTime = transTime


    def appendTaskDetails(self,taskDetails):
        self.taskDetailsList.append(taskDetails)
    def getTaskDetailsByID(self,taskID):
        for i in range(0, len(self.taskDetailsList)):
            if(self.taskDetailsList[i].taskID==taskID):
                return self.taskDetailsList[i]

    #任务是已经被调度过
    def isScheduled(self,taskID):
        for i in range(0, len(self.taskDetailsList)):
            if (self.taskDetailsList[i].taskID == taskID):
                return True
        return False
    #任务现在是否可以调度
    def isCanScheduleNow(self,taskID):
        if (self.isScheduled(taskID)):  # 自己不能已经被调度过
            return False
        parentsList = myMathTool.getParents(taskID, self.dag)
        for i in range(0, len(parentsList)):
            if (not self.isScheduled(parentsList[i])):  # 父节点必须全部被调度了
                return False
        return True



    #获取其他虚拟机将任务传输到指定虚拟机后，任务的预计开始时间和实际可开始时间（考虑了传输延迟）
    def getTimePY(self,taskID,vmInstance):#The time when parent's tasks performed by other virtual machines are completed and transmitted to the specified virtual machine
        parentsList = myMathTool.getParents(taskID, self.dag)
        ptime=0
        rtime=0
        for i in range(0,len(parentsList)):
            parentTaskDetails = self.getTaskDetailsByID(parentsList[i])
            if(parentTaskDetails.vmInsID!=vmInstance.instanceID):
                ptemp=parentTaskDetails.preEndTime + self.transTime[parentsList[i]][taskID]
                if(ptemp>ptime):
                    ptime=ptemp
                rtemp = parentTaskDetails.reaEndTime + self.transTime[parentsList[i]][taskID]
                if (rtemp > rtime):
                    rtime=rtemp
        return [ptime,rtime]



    #获取父节点完成时间加上传输延迟后，任务预计可开始时间和实际可开始时间，用于创建新的虚拟机的情况
    def getTimeAllwitTT(self,taskID):
        parentsList = myMathTool.getParents(taskID, self.dag)
        ptime = 0
        rtime = 0
        for i in range(0, len(parentsList)):
            parentTaskDetails = self.getTaskDetailsByID(parentsList[i])
            ptemp = parentTaskDetails.preEndTime + self.transTime[parentsList[i]][taskID]
            if (ptemp > ptime):
                ptime = ptemp
            rtemp = parentTaskDetails.reaEndTime + self.transTime[parentsList[i]][taskID]
            if (rtemp > rtime):
                rtime = rtemp
        return [ptime, rtime]



    #获取接下来可以调度的队列
    def getNextQue(self):
        tempQueue = []
        queue=[]
        for i in range(0,len(self.taskDetailsList)):
            tempQueue.extend(myMathTool.getChildren(self.taskDetailsList[i].taskID,self.dag))
        tempQueue = list(set(tempQueue))#去重复
        for j in range(0,len(tempQueue)):
            if(self.isCanScheduleNow(tempQueue[j])):
                queue.append(tempQueue[j])
        return queue

