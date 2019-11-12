from flask import Flask, jsonify, make_response, request, abort
from consumer import *

app = Flask(__name__)
listaConsumer = []
listaSalas = []

@app.route('/historico', methods=['GET'])
def get_historicos():
    print("## GET_USERS")
    
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
def get_historico(id):
    print("## GET_USER")
    
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
    print(ret_json)
    return jsonify({'historico': ret_json})
    
@app.route('/consumer', methods=['POST'])
def post_user():
    if not request.json or not 'id' in request.json:
        abort(400)
    
    listaConsumer.append(consumer(int(request.json['id'])))
    listaConsumer[-1].start()
    listaSalas.append(int(request.json['id']))
    
    return jsonify({'consumer': int(request.json['id'])})
    
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
