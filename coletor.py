import sys
import json
import zmq
import time

def calc_media(vetor):
    total = 0
    i = 0.0
    for valor in vetor:
        i += 1.0
        total += valor["valor"]
    return total / i

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")

context2 = zmq.Context()
socketPUB = context2.socket(zmq.PUB)
socketPUB.bind("tcp://*:5557")

if len(sys.argv) == 1:
    print("Lendo todas as salas")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    
else:
    sala = str(sys.argv[1])
    print("Lendo a sala {0}".format(sala))
    socket.setsockopt_string(zmq.SUBSCRIBE, sala)
    
valores = []
media = 0.0
    
while True:
    raw_msg = socket.recv_string()
    
    msg = json.loads(raw_msg.split(' ', 1)[1])
    dado = {
            "sala": msg["sala"],
            "valor": msg["valor"]
            }
    print("SALA {0} ::: TEMP ATUAL {1:.2f}º".format(dado["sala"], dado["valor"]))
    
    valores.append(dado)
    if len(valores) > 10:
        valores = valores[1:]
    
    media = calc_media(valores)
    
    print("Média da sala: {0:.2f}º".format(media))
    
    payload = json.dumps({"sala": dado["sala"], "timestamp": time.localtime(), "temp": media})
    socketPUB.send_string("{topico} {payload}".format(topico = dado["sala"], payload = payload))
