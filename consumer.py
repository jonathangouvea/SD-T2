import sys
import json
import zmq
import time
import threading
import pandas as pd

class consumer():
    def __init__(self, id = ''):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5556")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, str(id))
        
        self.basedados = []
        self.basemedias = []
        self.valores = []
        self.read_lock = threading.Lock()
        
        self.started = False
        
    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self
        
    def subscribe(self):
        raw_msg = self.socket.recv_string()
    
        msg = json.loads(raw_msg.split(' ', 1)[1])
        with self.read_lock:
            self.basedados.append([msg["sala"], time.strftime('%X %x %Z'), msg["valor"]])
            self.valores.append(msg["valor"])
            if len(self.basedados) > 10:
                self.basedados = self.basedados[-10:]
                self.valores = self.valores[-10:]
                
            #print(sum(self.valores) / len(self.basedados))
                
            self.basemedias.append([
                msg["sala"], 
                time.strftime('%X %x %Z'), 
                sum(self.valores) / len(self.basedados)
            ])
            
            #print(self.basemedias)
            
    def update(self):
        while self.started:
            self.subscribe()
            
    def read(self):
        with self.read_lock:
            return self.basemedias
            
    def stop(self):
        self.started = False
        self.thread.join()
        
    def __exit__(self, exec_type, exc_value, traceback):
        self.socket.close()
