import zmq
import sys
import pickle
import time
import json
from random import gauss, randrange

if len(sys.argv) == 1:
    print("Faltam argumentos!\nExecute: python sensor.py <qtd_salas>")
    quit()
    
qtdSalas = str(sys.argv[1])

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

temperaturaSalas = []

for i in range(int(qtdSalas)):
    temperaturaSalas.append(randrange(10, 35))

print("Iniciando medição de {0} salas".format(qtdSalas))

while True:
    for i in range(int(qtdSalas)):
        temperaturaSalas[i] = gauss(temperaturaSalas[i], 1.5)
        payload = json.dumps({"sala": str(i+1), "valor": temperaturaSalas[i]})
        socket.send_string("{topico} {payload}".format(topico = str(i+1), payload = payload))
        print("Enviado [{0}, {1}]".format(str(i+1), payload))
    time.sleep(5)
