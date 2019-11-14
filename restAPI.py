from flask import Flask, jsonify, make_response, request, abort
from consumer import *

app = Flask(__name__)
listaConsumer = []
listaSalas = []

@app.route('/recente', methods=['GET'])
def getRecentes():
    ret_json = []
    for i in range(len(listaSalas)):
        ret_json.append({
            "sala": listaSalas[i],
            "temp": listaConsumer[i].read_last()
        })
    return jsonify({'recente': ret_json})

@app.route('/historico', methods=['GET'])
def getHistoricos():
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
    
@app.route('/consumer', methods=['POST'])
def postUser():
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
    return make_response(jsonify({'error': 'Not found'}), 404)
    
if __name__ == '__main__':
    listaConsumer.append(consumer(1))
    listaConsumer[-1].start()
    listaSalas.append(1)
    
    listaConsumer.append(consumer(2))
    listaConsumer[-1].start()
    listaSalas.append(2)
    
    app.run(port = 5000)
