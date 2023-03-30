from pymantic import sparql
import time
import threading

server = sparql.SPARQLServer('http://127.0.0.1:9999/blazegraph/sparql')

'''
server.update('load <file:///E:/KG_telecom_actions_1_.nq>')
server.update('load <file:///E:/KG_telecom_device_1_.nq>')
'''


def query(queryTxt):
    start = time.time()
    res1 = server.query(queryTxt)
    end = time.time()
    return [res1, end - start]   
   

def request():
    server1 = sparql.SPARQLServer('http://127.0.0.3:9999/blazegraph/sparql')
    print('Request started')
    start = time.time()
    server1.query('select * where {?s ?p ?o} limit 200000')
    end = time.time()
    print(end - start)

timer = time.time()
timeCounter = timer
array = []
currentThreadNum = 0  
threadcount = 20    #количество потоков
timeOfWorking = 5   #время работы
delta = 0.1          #переодичность запуска потоков

for i in range(threadcount):
    array.append(threading.Thread(target=request))
while(time.time() < timer + timeOfWorking):
    if(time.time() > timeCounter + delta):
        timeCounter = time.time()
        if(currentThreadNum < threadcount - 1):
            currentThreadNum = currentThreadNum + 1
            print(currentThreadNum, time.time() - timer) #выводит номер потока и время запуска
            array[currentThreadNum].start()