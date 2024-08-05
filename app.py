from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import time
import threading
import requests

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
    print('Servidor Websocket Python 1.0 - rodando...')
    print('==Socket.io==')
    print('port:5011')
    
    # BITCOIN Start the message sending thread
    # thread = threading.Thread(target=send_message)
    # thread.daemon = True
    # thread.start()
    
    # Run the Flask app
    #socketio.run(app, host='0.0.0.0', port=5011)
    socketio.run(app, host='0.0.0.0', port=5011)