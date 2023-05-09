from blazegraph_python_master.pymantic import sparql
import time
import threading
import statistics

class Pacific():
    def __init__(self, url):
        self.server = sparql.SPARQLServer(url)
        self.requests = []
        self.flag = 0
        self.countDeleteThreads = 1
        self.arrayThreads = []
        self.currentDeleteThreads = 0
        self.pauseTime = 0
        self.duration = []
        
    def append(self, request):
        if type(request) == str:
            self.requests.append(request)
        if type(request) == list:
            self.requests.extend(request)
    
    def status(self) -> list:
        return [self.flag,len(self.requests)]

    def deleteRequest(self, threadNum):
            num = threadNum
            start = 0
            end = 0
            self.currentDeleteThreads += 1
            while len(self.requests) != 0 and self.arrayThreads[num][1] == 1:
                request = self.requests.pop()
                start = time.time()
                self.server.update(request)
                end = time.time()
                self.duration.append(end - start)
                time.sleep(self.pauseTime)
            self.arrayThreads[num][1] = 0    
            self.currentDeleteThreads -= 1
            
    def start(self):
        print("+")               
        for i in range(self.countDeleteThreads):
            self.arrayThreads.append([threading.Thread(target=self.deleteRequest, args = (i,)),1])
        for thread in self.arrayThreads:
            thread[0].start()
        threading.Thread(target=self.manager())
        print("-")
            
    def manager(self):
        print("manager app")
        while len(self.duration) < 20:
            time.sleep(1)
        a = statistics.mean(self.duration)
        b = a
        self.flag = 1
        print("pacific info: ",self.flag, a, b)
        while b < a * 2:
            self.duration = []
            thread = threading.Thread(target=self.deleteRequest, args = (len(self.arrayThreads) - 1,))
            thread.start()
            self.arrayThreads.append([thread,1])
            while len(self.duration) < 10:
                time.sleep(1)
            b = statistics.mean(self.duration)
            print("pacific info: ",self.flag, a, b)
        self.flag = 2
        while b > a * 1.2:
            self.duration = []
            self.pauseTime += 0.5
            while len(self.duration) < 20:
                time.sleep(1)
            b = statistics.mean(self.duration)
            print("pacific info: ",self.flag, a, b)
        self.flag = 3
        print("results: threads - ", len(self.arrayThreads), ", pause - ", self.pauseTime)
        for thread in self.arrayThreads:
            thread[0].join()
        self.flag = 4
        print("pacific work: ", statistics.mean(self.duration))
        