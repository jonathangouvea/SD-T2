from flask import Flask, render_template, g, redirect, flash, Blueprint, request, session, url_for
import requests

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get('http://localhost:5000/historico/' + '1').json()['historico']
    
    temps = [resp['temp'] for resp in response]
    timestamps = [resp['timestamp'] for resp in response]
    print(temps)
    return render_template('website.html', temps = temps, timestamps = timestamps, sala = 1)

@app.route('/sala/<int:id>')
def sala(id):
    response = requests.get('http://localhost:5000/historico/' + str(id)).json()['historico']
    
    temps = [resp['temp'] for resp in response]
    timestamps = [resp['timestamp'] for resp in response]
    print(temps)
    return render_template('website.html', temps = temps, timestamps = timestamps, sala = id)
    
    return render_template('website.html', dados = response, sala = id)
    
if __name__ == '__main__':
    app.run(port = 5001, debug = True)
