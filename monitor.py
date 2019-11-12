import sys
import json
import zmq
import time
import threading
import pandas as pd

class monitorador():
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5557")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        self.basedados = []
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
            self.basedados.append([msg["sala"], msg["timestamp"], msg["temp"]])
        
    def update(self):
        while self.started:
            self.subscribe()
            
    def read(self):
        with self.read_lock:
            return self.basedados
            
    def stop(self):
        self.started = False
        self.thread.join()
        
    def __exit__(self, exec_type, exc_value, traceback):
        self.socket.close()
        
def print_base(base):
    if len(base) == 0: return
    for b in base:
        print("SALA {0}".format(b[0]), end="\t")
        print("TEMPERATURA MÉDIA {0:.2f}".format(b[2]), end="\t")
        print("HORÁRIO {0}/{1}/{2} {3}:{4}:{5}".format(b[1][2], b[1][1], b[1][0], b[1][3], b[1][4], b[1][5] ))
        #print("HORÁRIO {0}".format(time.strftime('%m%d_%H%M', b[1])))
    print("\n")
        
if __name__ == '__main__':
    M = monitorador()
    M.start()
    
    while True:
        sala = int(input("0. Mostrar todo o histórico\nN. Mostrar o histórico da sala N\n-1. Sair\n::: "))
        b = M.read()
        
        if sala < 0:
            M.stop()
            break
        
        if sala == 0:
            print_base(b)
            
        else:
            P = pd.DataFrame(b)
            p = P[P[0] == str(sala)]
            print_base(p.values.tolist())
    
    
    
    
    
    

