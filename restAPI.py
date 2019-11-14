"""
Arquivo com a RestAPI, contendo funções para criação e leitura dos consumidores e retorno em formato JSON para clientes externos.
"""

from flask import Flask, jsonify, make_response, request, abort
from consumer import *

app = Flask(__name__)
listaConsumer = []
listaSalas = []

@app.route('/recente', methods=['GET'])
def getRecentes():
    """Função que retorna as informações de última temperatura registrada de todas as salas
    """
    
    ret_json = []
    for i in range(len(listaSalas)):
        ret_json.append({
            "sala": listaSalas[i],
            "temp": listaConsumer[i].read_last()
        })
    return jsonify({'recente': ret_json})

@app.route('/historico', methods=['GET'])
def getHistoricos():
    """Função que retorna em JSON o histórico de todas as temperaturas registradas em todas as salas
    """
    
    ret_dataset = []
    for consumer in listaConsumer:
        ret_dataset.extend(consumer.read())
    
    ret_json = []
    for ret in ret_dataset:
        ret_json.append({
            "sala": ret[0],
            "timestamp": ret[1],
            "temp": ret[2]
        })
    
    return jsonify({'historico': ret_json})
    
@app.route('/historico/<int:id>', methods=['GET'])
def getHistorico(id):    
    """Função que retorna em JSON o histórico de uma sala específica. Primeiro a função encontra o consumidor associado a essa sala e depois faz a leitura dos dados
    """
    
    ret_dataset = []
    for i in range(len(listaSalas)):
        if id == listaSalas[i]:
            ret_dataset.extend(listaConsumer[i].read())
    
    ret_json = []
    for ret in ret_dataset:
        ret_json.append({
            "sala": ret[0],
            "timestamp": ret[1],
            "temp": ret[2]
        })
    return jsonify({'historico': ret_json})
    
@app.route('/sala', methods=['POST'])
def postSala():
    """Função que cria um consumidor de uma sala e retorna o código de qual a sala criada. Caso receba por POST um ID ele irá criar um consumidor associado a esse ID
    """
    
    if not request.json or not 'id' in request.json:
        id = listaSalas[-1] + 1
    else:
        id = int(request.json['id'])
    
    listaConsumer.append(consumer(id))
    listaConsumer[-1].start()
    listaSalas.append(id)
    
    return jsonify({'consumer': id})
    
    
@app.errorhandler(404)
def not_found(error):
    """Função padrão em caso de erro not found
    """
    
    return make_response(jsonify({'error': 'Not found'}), 404)
    
if __name__ == '__main__':
    """Inicialização da API, precedida pela criação de dois consumidores associados às salas 1 e 2
    """
    
    listaConsumer.append(consumer(1))
    listaConsumer[-1].start()
    listaSalas.append(1)
    
    listaConsumer.append(consumer(2))
    listaConsumer[-1].start()
    listaSalas.append(2)
    
    app.run(port = 5000)
