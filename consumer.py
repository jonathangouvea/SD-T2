import sys
import json
import zmq
import time
import threading
import pandas as pd

class consumer():
    """Classe responsável por fazer a leitura das temperaturas de uma sala, e armazenar as médias das últimas 10 temperaturas.
    Ele irá se conectar ao PRODUCER e receber os dados dele, na sala/tópico desejado. Ele utiliza Threads para se manter ativo e armazena até 50 temperaturas por vez, para evitar preencher toda a memória. Ele retorna essa base de temperaturas ou a última temperatura média.    
    """
    
    def __init__(self, id = ''):
        """Função de inicialização. Caso receba um ID ele irá ler as mensagens/medições apenas desse tópico/sala, caso contrário ele lê todas as salas.
        """
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5556")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, str(id))
        
        self.temperaturasMedias = []
        self.ultimaTemperatura = "?"
        self.baseTemperaturas = []
        self.readLock = threading.Lock()
        
        self.started = False
        
    def start(self):
        """Função para início da leitura contínua de dados. Inicia a Thread para a função UPDATE
        """
        
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self
        
    def subscribe(self):
        """Função que realiza a leitura e armazenamento dos dados nas variáveis necessárias. 
        """
        
        raw_msg = self.socket.recv_string()
        msg = json.loads(raw_msg.split(' ', 1)[1])
        
        self.baseTemperaturas.append(msg["valor"])
        if len(self.baseTemperaturas) > 10:
            self.baseTemperaturas = self.baseTemperaturas[-10:]
        
        with self.readLock:
            self.temperaturasMedias.append([
                msg["sala"], 
                time.strftime('%X'), #Horário atual
                "{:.2f}".format(sum(self.baseTemperaturas) / len(self.baseTemperaturas))
            ])
            
            if len(self.temperaturasMedias) > 50:
                self.temperaturasMedias = self.temperaturasMedias[-50:]
            
            self.ultimaTemperatura = "{:.2f}".format(sum(self.baseTemperaturas) / len(self.baseTemperaturas))
            
            
    def update(self):
        """Função do loop para chamada da função de recebimento e escrita de dados
        """
        
        while self.started:
            self.subscribe()
            
    def read(self):
        """Função que retorna a base de dados de Temperaturas Médias. Aguarda a liberação do semáforo para evitar leitura e escrita ocorrendo ao mesmo tempo
        """
        
        with self.readLock:
            return self.temperaturasMedias
    
    def read_last(self):
        """Função que retorna a última temperatura média registrada. Aguarda a liberação do semáforo para evitar leitura e escrita ocorrendo ao mesmo tempo
        """
        
        with self.readLock:
            return self.ultimaTemperatura
            
    def stop(self):
        """Função para parada da thread
        """
        
        self.started = False
        self.thread.join()
        
    def __exit__(self, exec_type, exc_value, traceback):
        """Tratamento do fim do consumidor
        """
        
        self.stop()
        self.socket.close()
