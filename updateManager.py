from blazegraph_python_master.pymantic import sparql
import os

server = sparql.SPARQLServer('http://172.18.6.27:9999/blazegraph/sparql')

def clearDB():
    if os.path.isfile('E:/FQW/blazegraph.jnl'): 
        os.remove('E:/FQW/blazegraph.jnl') 
        print("DB cleared.")

def load0():
    with open('E:/FQW/0/load_script.TXT','r') as f:
        requests = f.readlines()
        for request in requests:
            server.update(request)
            print(request + "done")

def load1():
    with open('E:/FQW/1/load_script.TXT','r') as f:
        requests = f.readlines()
        for request in requests:
            server.update(request)
            print(request + "done")

def load2():
    with open('E:/FQW/2/load_script.TXT','r') as f:
        requests = f.readlines()
        for request in requests:
            server.update(request)
            print(request + "done")
load2()