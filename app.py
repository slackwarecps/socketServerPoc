import eventlet
eventlet.monkey_patch()
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import os
import uuid
import pymongo
from pymongo import MongoClient
from datetime import datetime

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app, async_mode=async_mode)
socketio = SocketIO(app, async_mode='eventlet')
thread = None
thread_lock = Lock()



# Configuração do MongoDB usando variáveis de ambiente
MONGO_DB_DATABASE = os.getenv('MONGO_DB_DATABASE', 'SUA_BASE_DE_DADOS')
MONGO_DB_URI = os.getenv('MONGO_DB_URI', 'SUA_URI_DO_MONGODB')


# Configuração do MongoDB
client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_DATABASE]
collection = db['socketclientes']

clients = {}

def setup():
    # Certifique-se de que a conexão com o MongoDB está configurada corretamente
    global client, db, collection
    client = MongoClient(MONGO_DB_URI)
    db = client[MONGO_DB_DATABASE]
    collection = db['socketclientes']
    
    
    
@app.before_request
def before_request():
    print('before_request')
    if not hasattr(app, 'setup_done'):
        setup()
        app.setup_done = True    
    


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count})


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/sessions')
def sessions_page():
    return render_template('sessions.html', async_mode=socketio.async_mode)

@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.event
def my_broadcast_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

# Sala ENTRANDO...
@socketio.event
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    print('join', message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

# Sala SAINDO...
@socketio.event
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room')
def on_close_room(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         to=message['room'])
    close_room(message['room'])


@socketio.event
def my_room_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         to=message['room'])


@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.event
def my_ping():
    emit('my_pong')


@socketio.event
def connect():
    print(f'Cliente conectado[sid]: {request.sid}')
    client_id_sessao = request.sid
    client_id = str(uuid.uuid4())
    codigo_cliente = request.headers.get('meu-codigo')
    if codigo_cliente is None:
        print( "ERRO DE HEADER")
        # sid_to_disconnect = None
        # for sid, cid in clients.items():
        #     if cid == client_id_sessao:
        #         sid_to_disconnect = sid
        #         break
        # client_id = clients.pop(client_id_sessao, None)
        kick_user(client_id_sessao)
        #disconnect(force=True)
        #disconnect_client()
        #raise ValueError("Valor do meu-codigo não fornecido")
        
    else:
        print('Codigo do cliente:', codigo_cliente)  
        timestamp = datetime.now()
        clients[request.sid] = client_id
        print(f'Cliente conectado: {client_id}')
        client_info = {
            "client_id": client_id,
            "codigo_cliente": codigo_cliente,
            "timestamp": timestamp
        }
        print('Informações do cliente:', client_info)
        
        # Inserir registro no MongoDB
        collection.insert_one(client_info)
        print('Registro CRIADO', client_info)
        emit('my_response', {'data': 'Connected', 'count': 0})


# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected', request.sid)
    
    
    
@socketio.event
def disconnect(force=False):
    if force:
        client_id = clients.pop(request.sid, None)
        print('Cliente desconectado forçadamente')
    else:
        client_id = clients.pop(request.sid, None)
        if client_id:
            print(f'Cliente desconectado: {client_id}')
            
            # Remover registro do MongoDB 
            collection.delete_one({'client_id': client_id})
            print('Registro REMOVIDO', client_id)
            
        
            print('Informações do cliente:', client_id)
            emit('my_response', {'data': 'Disconnected', 'info': client_id})
            
            
def kick_user(sid):
    socketio.server.disconnect(sid)
    print(f"Usuario {sid} foi BANIDO  kicked out.")
    print("****************************************")



if __name__ == '__main__':
    minha_porta = int(os.environ.get('PORT', 80))  # Get port from environment variable
    gunicorn_options = {
        'workers': 3,  # Adjust worker count as needed
     }
    #socketio.run(app, allow_unsafe_werkzeug=True)
    print('Servidor Websocket Python 1.4 - rodando...')
    print('==Socket.io==')
    print('==COMPLETAO==')
    print('minha_porta:'+str(minha_porta))
    

    #socketio.run(app,allow_unsafe_werkzeug=True, **gunicorn_options)
    #socketio.run(app,host='0.0.0.0',port=minha_porta)
    #socketio.run(app)
    socketio.run(app, host='0.0.0.0', port=80)