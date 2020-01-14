import mathModule as myMathTool
import VMMoudule as myVMtool
import DataPro as mydataPro



class CPAVE():
    def __init__(self,dag,transTimeArr,taskTypeArr,Deadline,VMDATAS):
        self.taskTypeArr=taskTypeArr
        self.deadLine=Deadline
        self.dag=dag
        self.transTimeArr=transTimeArr
        self.vmPool=myVMtool.VmPool()
        self.taskListAssistant=myVMtool.TaskListAssistant(dag,transTimeArr)
        self.VMDATAS=VMDATAS

    def start(self,startTime):

        #第一个任务的执行，创建虚拟机
        entrys = myMathTool.getEnrty(self.dag)
        taskID=entrys[0]
        tempCPPath = myMathTool.getCPave(self.dag, taskID, self.taskTypeArr)
        minSP = float("inf")
        vmInstance = -1
        for j in range(0, len(self.VMDATAS)):
            tempVMinstance = myVMtool.VmInstance()
            tempVMinstance.createNewVM(j + 1, startTime, self.VMDATAS)  # 参数为虚拟机内别、开始时间
            tempPstart = tempVMinstance.exIdeleTime  # 任务的预计开始时间,入口处任务随虚拟机可用开始
            tempPRuntime = tempVMinstance.pathRunTimeWithAve(taskTypeArr=self.taskTypeArr,
                                                             TaskSet=tempCPPath)  # 关键路径执预计执行时间
            tempPExTask = tempVMinstance.taskRunTimeWithAve(taskType=self.taskTypeArr[taskID])
            tempMS = tempPstart + tempPRuntime - startTime  # 关键路径makespan
            tempSP = tempPExTask * tempVMinstance.VMDATA["price"]  # 关键路径花费
            if (tempMS < self.deadLine and tempSP < minSP):
                vmInstance = tempVMinstance
                minSP = tempSP
        if (minSP == float("inf")):
            print("请重新设置DeadLine,DeadLine低于最小MS")
            return -1,-1

        # 模拟当前任务的执行时间
        taskDetails = myVMtool.TaskDetails(taskID, self.taskTypeArr[taskID])
        taskTimeArr = [vmInstance.exIdeleTime, vmInstance.realIdeleTime]  # 任务父节点都传输过来的时间[预计，实际]，入口处无父节点，即为虚拟机可用时间
        self.vmPool.appendVmInstance(vmInstance)
        vmInstance.runTask(taskDetails, taskTimeArr)
        self.taskListAssistant.appendTaskDetails(taskDetails)

        #其他入口任务是否满足基本DeadLine
        scheduleQueue = entrys[1:]
        #检测deadLine是否过分
        for i in range(0, len(scheduleQueue)):
            taskID=scheduleQueue[i]#index
            tempCPPath=myMathTool.getCPave(self.dag,taskID,self.taskTypeArr)
            minSP = float("inf")
            vmInstance = -1
            for j in range(0, len(self.VMDATAS)):
                tempVMinstance =myVMtool.VmInstance()
                tempVMinstance.createNewVM(j+1,startTime, self.VMDATAS)  # 参数为虚拟机内别、开始时间
                tempPstart = tempVMinstance.exIdeleTime  #任务的预计开始时间,入口处任务随虚拟机可用开始
                tempPRuntime=tempVMinstance.pathRunTimeWithAve(taskTypeArr=self.taskTypeArr,TaskSet=tempCPPath)#关键路径执预计执行时间
                tempPExTask=tempVMinstance.taskRunTimeWithAve(taskType=self.taskTypeArr[taskID])
                tempMS = tempPstart + tempPRuntime-startTime#关键路径makespan
                tempSP=tempPExTask* tempVMinstance.VMDATA["price"]#关键路径花费
                if (tempMS < self.deadLine and  tempSP < minSP):
                    vmInstance = tempVMinstance
                    minSP = tempSP
            if (minSP == float("inf")):
                print("请重新设置DeadLine,DeadLine低于最小MS")
                return -1,-1

        # 任务调度开始
        # 循环到调度列表为空
        # 任务调度开始
        # 循环到调度列表为空
        if(len(scheduleQueue)==0):
            return -1,-1
        while (True):
            for i in range(0, len(scheduleQueue)):

                # 获取关键路径，总任务规模
                taskID = scheduleQueue[i]
                tempCPPath = myMathTool.getCPave(self.dag,taskID,self.taskTypeArr)
                # 模拟调度，使用的是预计的父亲节点完成时间来调度
                # 已有虚拟机,
                temp_1_minsp = float("inf")
                temp_1_timeArr = -1
                temp_1_vminstance = -1
                for index in range(0, len(self.vmPool.vmList)):
                    vmInstanceHave = self.vmPool.vmList[index]
                    tempTimeArr = self.taskListAssistant.getTimePY(taskID, vmInstanceHave)  # 【预计，实际】，父节点结果传输到该虚拟机的时间
                    if (vmInstance.isAvailable):  # 虚拟机没有被释放,虚拟机可用
                        taskPreStartTime = max(tempTimeArr[0],
                                               vmInstanceHave.exIdeleTime)  # 任务预计可以开始时间，虚拟机预计空闲时间和任务预计可以开始时间，取最大
                        tempPRuntime = vmInstanceHave.pathRunTimeWithAve(taskTypeArr=self.taskTypeArr,TaskSet=tempCPPath)
                        tempMS = taskPreStartTime + tempPRuntime - startTime
                        tempPExTask = vmInstanceHave.taskRunTimeWithAve(taskType=self.taskTypeArr[taskID])


                        tempCost =  tempPExTask * vmInstanceHave.VMDATA["price"]
                        if (tempMS < self.deadLine and tempCost < temp_1_minsp):
                            temp_1_minsp = tempCost
                            temp_1_vminstance = vmInstanceHave
                            temp_1_timeArr = tempTimeArr
                        # print("task id", taskID, tempMS)
                # 创建新的虚拟机的情况
                temp_2_vmInstance = -1
                temp_2_minsp = float("inf")
                temp_2_timeArr = self.taskListAssistant.getTimeAllwitTT(taskID)
                for j in range(0, len(self.VMDATAS)):
                    tempVMinstance = myVMtool.VmInstance()
                    tempVMinstance.createNewVM(j+1,temp_2_timeArr[0], self.VMDATAS)  #
                    tempPstart = max(temp_2_timeArr [0], tempVMinstance.exIdeleTime)  # 任务的预计开始时间
                    tempPRuntime = tempVMinstance.pathRunTimeWithAve(taskTypeArr=self.taskTypeArr,TaskSet=tempCPPath)
                    tempMS = tempPstart + tempPRuntime - startTime
                    tempPExTask = tempVMinstance.taskRunTimeWithAve(taskType=self.taskTypeArr[taskID])

                    tempSP = tempPExTask * tempVMinstance.VMDATA["price"]
                    # 该情况满足DeadLine，同时记录花费最小的情况
                    if (tempMS < self.deadLine and tempSP < temp_2_minsp):
                        temp_2_vmInstance = tempVMinstance
                        temp_2_minsp = tempSP
                    # print(tempPstart,tempCPPath,self.taskTypeArr[taskID])
                    # print("task id", taskID,tempPstart, tempMS,tempPRuntime)
                # 模拟执行
                # 在已有虚拟机上执行
                if (temp_1_minsp <= temp_2_minsp and temp_1_minsp != float("inf")):
                    taskDetails = myVMtool.TaskDetails(taskID, self.taskTypeArr[taskID])
                    temp_1_vminstance.runTask(taskDetails, temp_1_timeArr)
                    self.taskListAssistant.appendTaskDetails(taskDetails)
                # 在新建虚拟机上执行
                if (temp_2_minsp < temp_1_minsp and temp_2_minsp != float("inf")):
                    taskDetails = myVMtool.TaskDetails(taskID, self.taskTypeArr[taskID])
                    self.vmPool.appendVmInstance(temp_2_vmInstance)
                    temp_2_vmInstance.runTask(taskDetails, temp_2_timeArr,)
                    self.taskListAssistant.appendTaskDetails(taskDetails)
                # 如果已经不满足DeadLine了，使用最快的虚拟机
                if (temp_1_minsp == float("inf") and temp_2_minsp == float("inf")):
                    print("任务序号",taskID,"任务类型",self.taskTypeArr[taskID],"预计开始时间",temp_2_timeArr[0],"实际开始时间",temp_2_timeArr[1],"已经不满足DeadLine了，使用最快的虚拟机")
                    temp_3_vmInstance = -1
                    temp_3_ms = float("inf")
                    temp_3_timeArr = self.taskListAssistant.getTimeAllwitTT(taskID)
                    for j in range(0, len(self.VMDATAS)):
                        tempVMinstance = myVMtool.VmInstance()
                        tempVMinstance.createNewVM(j+1, temp_3_timeArr[0],self.VMDATAS)  # 参数为虚拟机内别、任务的预计开始时间，实际开始时间  自己确定租用虚拟机的时间
                        tempPstart = max(temp_3_timeArr[0], tempVMinstance.exIdeleTime)  # 任务的预计开始时间
                        tempPRuntime = tempVMinstance.pathRunTimeWithAve(taskTypeArr=self.taskTypeArr,TaskSet=tempCPPath)
                        tempMS = tempPstart + tempPRuntime - startTime
                        # 找到MS最小的情况
                        if (tempMS < temp_3_ms):
                            temp_3_ms = tempMS
                            temp_3_vmInstance = tempVMinstance

                    taskDetails = myVMtool.TaskDetails(taskID, self.taskTypeArr[taskID])
                    self.vmPool.appendVmInstance(temp_3_vmInstance)
                    temp_3_vmInstance.runTask(taskDetails, temp_3_timeArr)
                    self.taskListAssistant.appendTaskDetails(taskDetails)

            # 获取下个可调度列表
            scheduleQueue = self.taskListAssistant.getNextQue()
            if (len(scheduleQueue) == 0):
                break
        for i in range(0, len(self.vmPool.vmList)):
            self.vmPool.vmList[i].print()
        for i in range(0, len(self.taskListAssistant.taskDetailsList)):
            self.taskListAssistant.taskDetailsList[i].print()
        return self.vmPool, self.taskListAssistant

def CPDETEST():
    VMDATAS = mydataPro.getVMDATAS()
    dag, transTimeArr = myMathTool.getXMLtoDag("Montage24.xml", 24)
    taskTypeArr = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
    Deadline = 145
    my = CPAVE(dag, transTimeArr, taskTypeArr, Deadline, VMDATAS)
    vmpool, tasklist = my.start(0)

    # VMDATAS=mydataPro.getVMDATAS()
    # dag=[[0,1,1,0],[0,0,0,1],[0,0,0,1],[0,0,0,0]]
    # transTimeArr=[[0,1,1,0],[0,0,0,1],[0,0,0,1],[0,0,0,0]]
    # taskTypeArr=[1,2,3,1]
    # Deadline=100
    # my=CPAVE(dag,transTimeArr,taskTypeArr,Deadline,VMDATAS)
    # vmpool,tasklist=my.start(0)

CPDETEST()