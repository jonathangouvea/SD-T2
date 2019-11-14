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
        
        self.temperaturasMedias = []
        self.ultimaTemperatura = 0
        self.baseTemperaturas = []
        self.readLock = threading.Lock()
        
        self.started = False
        
    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self
        
    def subscribe(self):
        raw_msg = self.socket.recv_string()
        msg = json.loads(raw_msg.split(' ', 1)[1])
        
        self.baseTemperaturas.append(msg["valor"])
        if len(self.baseTemperaturas) > 10:
            self.baseTemperaturas = self.baseTemperaturas[-10:]
        
        with self.readLock:
            self.temperaturasMedias.append([
                msg["sala"], 
                time.strftime('%X'), 
                "{:.2f}".format(sum(self.baseTemperaturas) / len(self.baseTemperaturas))
            ])
            
            self.ultimaTemperatura = "{:.2f}".format(sum(self.baseTemperaturas) / len(self.baseTemperaturas))
            
            
    def update(self):
        while self.started:
            self.subscribe()
            
    def read(self):
        with self.readLock:
            return self.temperaturasMedias
    
    def read_last(self):
        with self.readLock:
            return self.ultimaTemperatura
            
    def stop(self):
        self.started = False
        self.thread.join()
        
    def __exit__(self, exec_type, exc_value, traceback):
        self.socket.close()
