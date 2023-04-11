from pymantic import sparql
import time
import psutil
import threading
import statistics
import matplotlib.pyplot as plt

server = sparql.SPARQLServer('http://127.0.0.1:9999/blazegraph/sparql')

arrayDelete = [['delete where {<http://127.0.0.1/Core_1_Level_2_1/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1000/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1001/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1002/> <http://127.0.0.1/bg/ont/test1#has_parent_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1003/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1004/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1005/> <http://127.0.0.1/bg/ont/test1#linked_to> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1006/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_50114/> <http://127.0.0.1/bg/ont/test1#has_parent_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_12128/> <http://127.0.0.1/bg/ont/test1#linked_to> ?o}'
         ]]



arrayInsert = [["insert data {<http://127.0.0.1/Core_1_Level_2_1/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1000/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1000'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1001/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1001'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1002/> <http://127.0.0.1/bg/ont/test1#has_parent_id> <http://127.0.0.1/Core_1/>}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1003/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1003'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1004/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1004'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1005/> <http://127.0.0.1/bg/ont/test1#linked_to> <http://127.0.0.1/Core_2_Level_2_1005/>}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1006/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1006'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_50114/> <http://127.0.0.1/bg/ont/test1#has_parent_id> <http://127.0.0.1/Core_1/>}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_12128/> <http://127.0.0.1/bg/ont/test1#linked_to> <http://127.0.0.1/Core_2_Level_2_12128/>}"
          ]]

arraySelect = [['select * where {?s ?p ?o} limit 50000','select * where {?s ?p ?o} limit 50000']]

flagDeleteThread = 0
numderDeleteArray = 0
flagSelectThread = 1
numderSelectArray = 0
flagCPUThread = 1
arrayThreads = []

def deleteRequest():
    number = numderDeleteArray
    executionTime = []
    for i in range(len(arrayDelete[number])):
        print("Delete request №" + str(i))
        start = time.time()
        #Удаление записи
        server.update(arrayDelete[number][i])
        end = time.time()
        executionTime.append(end - start)
    print("execution time of deletion requests: " + str(executionTime))
    print("average execution time: " + str(statistics.mean(executionTime)))

def selextRequest():
    number = numderDeleteArray
    executionTime = []
    for i in range(len(arraySelect[number])):
        print("Select request №" + str(i))
        start = time.time()
        #Удаление записи
        server.query(arraySelect[number][i])
        end = time.time()
        executionTime.append(end - start)
    print("execution time of deletion requests: " + str(executionTime))
    print("average execution time: " + str(statistics.mean(executionTime)))

def controlCPU():
    cpuArray = []
    timer = time.time()
    delta = 1
    while(flagCPUThread == 1):   
        if(time.time() > timer + delta):
            cpuArray.append(psutil.cpu_percent(interval=1, percpu=False))
            timer = time.time()
    print("cpu load: " + str(cpuArray))
    if(len(cpuArray) > 0):
        print("average cpu load: " + str(statistics.mean(cpuArray)))    #Выводит среднее время ответа
    
    

if(flagCPUThread == 1):
    thread = threading.Thread(target=controlCPU)
    thread.start()

#Запустит первый список selrct запросов из arraySelect на одном потоке
if(flagSelectThread == 1):
    numderSelectArray = 0
    numberThread = len(arrayThreads)
    arrayThreads.append(threading.Thread(target=selextRequest))
    arrayThreads[numberThread].start()

#Запустит все списки selrct запросов из arraySelect на разных потоках
if(flagSelectThread == 2):
    numberThread = len(arrayThreads)
    for i in range(len(arrayDelete)):
        arrayThreads.append(threading.Thread(target=selextRequest))
    for i in range(len(arrayDelete)):
        numderSelectArray = i
        arrayThreads[numberThread + i].start()

#Запустит первый список запросов удаления из arrayDelete на одном потоке
if(flagDeleteThread == 1):
    numderDeleteArray = 0
    numberThread = len(arrayThreads)
    arrayThreads.append(threading.Thread(target=deleteRequest))
    arrayThreads[numberThread].start()

#Запустит все списки запросов удаления из arrayDelete на разных потоках
if(flagDeleteThread == 2):
    numberThread = len(arrayThreads)
    for i in range(len(arrayDelete)):
        arrayThreads.append(threading.Thread(target=deleteRequest))
    for i in range(len(arrayDelete)):
        numderDeleteArray = i
        arrayThreads[numberThread + i].start()

 
if(flagCPUThread == 1):
    for thread in arrayThreads:
        thread.join()
    flagCPUThread = 0