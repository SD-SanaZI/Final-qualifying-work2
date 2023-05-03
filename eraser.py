from blazegraph_python_master.pymantic import sparql
import time
import psutil
import threading
import statistics

class Eraser():
    def __init__(self, url):
        self.server = sparql.SPARQLServer(url)
        self.requests = []
        self.presentCPU = 0
        self.currentCPU = 0
        self.flagCPUThread = 0
        self.countDeleteThreads = 1
        self.arrayThreads = []
        self.cpuThread = 0
        self.currentDeleteThreads = 0
    
    def append(self, request):
        if type(request) == str:
            self.requests.append(request)
        if type(request) == list:
            self.requests.extend(request)
    
    def status(self) -> list:
        return self.requests
    
    def controlCPU(self):
        cpuArray = []
        ramArray = []
        timer = time.time()
        delta = 1
        while self.flagCPUThread == 1:   
            if time.time() > timer + delta:
                cpuArray.append(psutil.cpu_percent())
                ramArray.append(psutil.virtual_memory().percent)
                timer = time.time()
                if len(cpuArray) > 4:
                    self.presentCPU = self.currentCPU
                    self.currentCPU = statistics.mean(cpuArray)
                    cpuArray = []

    def deleteRequest(self, threadNum):
            num = threadNum
            self.currentDeleteThreads += 1
            while len(self.requests) != 0 and self.arrayThreads[num][1] == 1:
                request = self.requests.pop()
#                print("Pull:", len(self.requests))
                self.server.update(request)
            self.arrayThreads[num][1] = 0    
            self.currentDeleteThreads -= 1
            
    def start(self):
        self.cpuThread = threading.Thread(target=self.controlCPU)
        self.flagCPUThread = 1
        self.cpuThread.start()                
        for i in range(self.countDeleteThreads):
            self.arrayThreads.append([threading.Thread(target=self.deleteRequest, args = (i,)),1])
        for thread in self.arrayThreads:
            thread[0].start()
        threading.Thread(target=self.manager())
            
    def manager(self):
        deltaTime = 6
        deltaThread = 5
        timer = time.time()
        while self.flagCPUThread == 1 :
            if time.time() > timer + deltaTime:
                timer = time.time()
                if self.presentCPU < self.currentCPU:
                    self.countDeleteThreads += deltaThread
                else:
                    self.countDeleteThreads -= deltaThread
                    for i in range(self.countDeleteThreads, self.countDeleteThreads + deltaThread):
                        if i > 1:
                            self.arrayThreads[i][1] = 0
                    if self.countDeleteThreads < 1:
                        self.countDeleteThreads = 1
                print("Threads: " + str(self.countDeleteThreads))
                print("Threads*: " + str(self.currentDeleteThreads))
                for i in range(self.countDeleteThreads - len(self.arrayThreads)):
                    thread = threading.Thread(target=self.deleteRequest, args = (len(self.arrayThreads) - 1,))
                    thread.start()
                    self.arrayThreads.append([thread,1])
                for i in range(self.countDeleteThreads):
                    if self.arrayThreads[i][0].isAlive() == False:
                        thread = threading.Thread(target=self.deleteRequest, args = (i,))
                        thread.start()
                        self.arrayThreads.append([thread,1])
            if len(self.requests) == 0:
                self.flagCPUThread = 0