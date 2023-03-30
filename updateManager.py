from pymantic import sparql
import time
import statistics
    
server = sparql.SPARQLServer('http://127.0.0.2:9999/blazegraph/sparql')

timer = time.time()
array1 = ['delete where {<http://127.0.0.1/Core_1_Level_2_1/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1000/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1001/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1002/> <http://127.0.0.1/bg/ont/test1#has_parent_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1003/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1004/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1005/> <http://127.0.0.1/bg/ont/test1#linked_to> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_1006/> <http://127.0.0.1/bg/ont/test1#has_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_50114/> <http://127.0.0.1/bg/ont/test1#has_parent_id> ?o}',
         'delete where {<http://127.0.0.1/Core_1_Level_2_12128/> <http://127.0.0.1/bg/ont/test1#linked_to> ?o}'
         ]

array2 = ["insert data {<http://127.0.0.1/Core_1_Level_2_1/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1000/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1000'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1001/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1001'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1002/> <http://127.0.0.1/bg/ont/test1#has_parent_id> <http://127.0.0.1/Core_1/>}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1003/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1003'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1004/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1004'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1005/> <http://127.0.0.1/bg/ont/test1#linked_to> <http://127.0.0.1/Core_2_Level_2_1005/>}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_1006/> <http://127.0.0.1/bg/ont/test1#has_id> 'Core_1_Level_2_1006'}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_50114/> <http://127.0.0.1/bg/ont/test1#has_parent_id> <http://127.0.0.1/Core_1/>}",
          "insert data {<http://127.0.0.1/Core_1_Level_2_12128/> <http://127.0.0.1/bg/ont/test1#linked_to> <http://127.0.0.1/Core_2_Level_2_12128/>}"]

array = []
count = 0
print('start')
while(count < len(array1)):
    print(count)
    start = time.time()
    #Удаление записи
    server.update(array1[count])
    end = time.time()
    array.append(end - start)
    count = count + 1
    
print(array)
print(statistics.mean(array))    #Выводит среднее время ответа

count = 0
while(count < len(array1)):
    server.update(array2[count])
    count = count + 1