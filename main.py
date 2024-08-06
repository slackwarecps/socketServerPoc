from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import time
import threading
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def fetch_bitcoin_price():
    response = requests.get('https://api.coinbase.com/v2/prices/btc-usd/spot')
    data = response.json()
    return data['data']['amount']

def send_message():
    while True:
        price = fetch_bitcoin_price()
        message = {
            "e": "trade",
            "E": int(time.time() * 1000),
            "s": "BTCUSD",
            "p": price
        }
        socketio.emit('bitcoin_price', json.dumps(message), namespace='/ws')
        #socketio.emit('bitcoin_price', json.dumps(message))
        #print("Message sent:", message)
        time.sleep(2)

@app.route('/')
def index():
    return "WebSocket server is running!"

@app.route('/opa')
def index_opa():
    return render_template('index.html')

@app.route('/sessions')
def index_sessions():
    return render_template('sessions.html')

@socketio.on('connect', namespace='/ws')
def handle_connect():
    print('Client connected')
    emit('bitcoin_price', json.dumps({"message": "Connected to WebSocket"}))

@socketio.on('disconnect', namespace='/ws')
def handle_disconnect():
    print('Client disconnected')
    
# Receive the test request from client and send back a test response
@socketio.on('test_message', namespace='/ws')
def handle_message(data):
    print('received message: ' + str(data))
    emit('test_response', {'data': 'Test response sent'})
    
#socketio.on_namespace(MyNamespace('/'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get port from environment variable
    gunicorn_options = {
        'workers': 3,  # Adjust worker count as needed
     }
    print('Servidor Websocket Python 1.2 - rodando...')
    print('==Socket.io==')
    print('port:'+os.environ.get('PORT'))

    #socketio.run(app,allow_unsafe_werkzeug=True, **gunicorn_options)
    socketio.run(app)


