from flask import Flask
from flask_socketio import SocketIO, emit
import json
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# JSON message to be sent
message = {
    "e": "trade",
    "E": 1722766102790,
    "s": "BTCUSDT",
    "t": 3718209179,
    "p": "60610.00000000",
    "q": "0.00154000",
    "T": 1722766102789,
    "m": True,
    "M": True
}

def send_message():
    while True:
        socketio.emit('greetings', json.dumps(message), namespace='/gs-guide-websocket')
        print(",, enviou...")
        time.sleep(2)

@app.route('/')
def index():
    return "WebSocket server is running!"

@socketio.on('connect', namespace='/gs-guide-websocket')
def handle_connect():
    print('Client connected')
    emit('greetings', json.dumps(message))

@socketio.on('disconnect', namespace='/gs-guide-websocket')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Start the message sending thread
    thread = threading.Thread(target=send_message)
    thread.daemon = True
    thread.start()
    
    # Run the Flask app
    socketio.run(app, host='0.0.0.0', port=5011)