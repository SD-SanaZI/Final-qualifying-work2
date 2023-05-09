from blazegraph_python_master.pymantic import sparql
import time
import psutil
import threading
import statistics
import matplotlib.pyplot as plt
import random

server = sparql.SPARQLServer('http://172.18.6.27:9999/blazegraph/sparql')

arrayDelete = []
arraySelect = []
arrayThreads = []
executionTimeSelect = []
executionTimeDelete = []
cpuThread = 0
deltaDelete = 0.5
settings = [[1,0,2,100,5,0,0,0]]

#            [1,1,1,100,5,150,1,0.5],
#            [1,1,1,100,5,150,1,1],
#            [1,1,1,100,5,150,1,2],
#            [1,1,1,100,5,150,1,3],

flagSelectThread = 0
flagDeleteThread = 0
flagCPUThread = 0
countSelectRequests = 0
countSelectThreads = 0
countDeleteRequests = 0
countDeleteThreads = 0


class Counter():
    def __init__(self):
        self.num = 0
    
    def get(self) -> int:
        self.num += 1
        print(self.num)
        return self.num - 1
    
    def current(self):
        return self.num

counterSelect = Counter()
counterDelete = Counter()

def createArraySelect(requests_size):
    for i in range(requests_size):
        query = 'select * where {?s ?p ?o} limit ' + str(random.randint(90000, 110000))
        arraySelect.append(query)

def createArrayDelete(requests_size, sample_size):
    result = server.query('select * where { ?s ?p ?o } limit ' + str(sample_size))
    if requests_size > len(result['results']['bindings']):
        requests_size = len(result['results']['bindings'])
    request_result = random.sample(result['results']['bindings'], requests_size)
    for i in request_result:
        s = i['s']['value']
        if 'http' in s:
            s = "<" + s + ">"
        p = i['p']['value']
        if 'http' in p:
            p = "<" + p + ">"
        o = i['o']['value']
        if 'http' in o:
            o = "<" + o + ">"
        else:
            o = "'" + o + "'"
        arrayDelete.append('delete where {' + s + ' ' + p + ' ' + o + '}')

def selextRequest():
    while counterSelect.current() < len(arraySelect):
#        time.sleep(1)
        start = time.time()
        print('s')
        server.query(arraySelect[counterSelect.get()])
        end = time.time()
        executionTimeSelect.append(end - start)
    arrayDelete = []

def selextRequest2():
    while(flagSelectThread == 1):
        start = time.time()
        print('s')
        server.query('select * where {?s ?p ?o} limit 100000')
        end = time.time()
        executionTimeSelect.append(end - start)

def deleteRequest(delta):
    while counterDelete.current() < len(arrayDelete):
        time.sleep(delta)
        start = time.time()
        print('d-------------------')
        server.update(arrayDelete[counterDelete.get()])
        end = time.time()
        executionTimeDelete.append(end - start)

def controlCPU():
    cpuArray = []
    ramArray = []
    timer = time.time()
    delta = 1
    while(flagCPUThread == 1):   
        if(time.time() > timer + delta):
            cpuArray.append(psutil.cpu_percent())
            ramArray.append(psutil.virtual_memory().percent)
            timer = time.time()
#    print("cpu load: " + str(cpuArray))
#    print("ram load: " + str(ramArray))
    if(len(cpuArray) > 0):
        print("average cpu load: " + str(statistics.mean(cpuArray)))    #Выводит среднее время ответа
        plt.title('CPU')
        plt.plot(cpuArray,"r")
        plt.plot([0,len(cpuArray)],[statistics.mean(cpuArray),statistics.mean(cpuArray)],'b')
        plt.show()
    if(len(ramArray) > 0):
        print("average ram load: " + str(statistics.mean(ramArray)))    #Выводит среднее время ответа
        plt.title('RAM')
        plt.plot(ramArray,"r")
        plt.plot([0,len(ramArray)],[statistics.mean(ramArray),statistics.mean(ramArray)],'b')
        plt.show()


for i in settings:
    print(i)
    counterSelect = Counter()
    counterDelete = Counter()
    arrayDelete = []
    arraySelect = []
    arrayThreads = []
    executionTimeSelect = []
    executionTimeDelete = []
    cpuThread = 0
    flagSelectThread = i[0]
    flagDeleteThread = i[1]
    flagCPUThread = i[2]
    countSelectRequests = i[3]
    countSelectThreads = i[4]
    countDeleteRequests = i[5]
    countDeleteThreads = i[6]
    deltaDelete = i[7]

    if(flagCPUThread == 1):
        cpuThread = threading.Thread(target=controlCPU)
        cpuThread.start()
        
    createArraySelect(countSelectRequests)
    createArrayDelete(countDeleteRequests,100000)
    
    if(flagSelectThread == 1):
#        createArraySelect(countSelectRequests)
        numberThread = len(arrayThreads)
        for i in range(countSelectThreads):
            arrayThreads.append(threading.Thread(target=selextRequest))
        for i in range(countSelectThreads):
            arrayThreads[numberThread + i].start()

    if(flagDeleteThread == 1):
#        createArrayDelete(countDeleteRequests,2000)
        numberThread = len(arrayThreads)
        for i in range(countDeleteThreads):
            arrayThreads.append(threading.Thread(target=deleteRequest, args=(deltaDelete,)))
        for i in range(countDeleteThreads):
            arrayThreads[numberThread + i].start()
    
    if(flagCPUThread != 0):
        while counterDelete.current() < len(arrayDelete):
            time.sleep(1)
        flagSelectThread = 0
        for thread in arrayThreads:
            thread.join()
        if(flagCPUThread == 1):
            flagCPUThread = 0
            cpuThread.join()
        if(len(executionTimeSelect) > 0):
#            print("execution time of selection requests: " + str(executionTimeSelect))
            print("average execution time: " + str(statistics.mean(executionTimeSelect)))
            plt.title('Select ' + str(countSelectRequests) + ' requests, ' + str(countSelectThreads) + ' threads')
            plt.plot(executionTimeSelect,"r")
            plt.plot([0,len(executionTimeSelect)],[statistics.mean(executionTimeSelect),statistics.mean(executionTimeSelect)],'b')
            plt.show()
        if(len(executionTimeDelete) > 0):
#            print("execution time of deletion requests: " + str(executionTimeDelete))
            print("average execution time: " + str(statistics.mean(executionTimeDelete)))
            plt.title('Delete ' + str(countDeleteRequests) + ' requests, ' + str(countDeleteThreads) + ' threads')
            plt.plot(executionTimeDelete,"r")
            plt.plot([0,len(executionTimeDelete)],[statistics.mean(executionTimeDelete),statistics.mean(executionTimeDelete)],'b')
            plt.show()
