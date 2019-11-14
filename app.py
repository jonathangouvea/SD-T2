from flask import Flask, render_template, g, redirect, flash, Blueprint, request, session, url_for, redirect
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('sala', id = 1))

@app.route('/sala/<int:id>')
def sala(id):
    response = requests.get('http://localhost:5000/historico/' + str(id)).json()['historico']
    temps = [resp['temp'] for resp in response]
    timestamps = [resp['timestamp'] for resp in response]
    
    response = requests.get('http://localhost:5000/recente').json()['recente']
    salas = [resp['sala'] for resp in response]
    last_temp = [resp['temp'] for resp in response]
    
    return render_template('website.html', temps = temps, timestamps = timestamps, sala = id, salas = salas, last_temp = last_temp)
    
@app.route('/nova')
def novaSala():
    response = requests.post('http://localhost:5000/consumer').json()
    return redirect(url_for('sala', id = response['consumer']))
    
if __name__ == '__main__':
    app.run(port = 5001, debug = True)
