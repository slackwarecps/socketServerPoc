# Servidor socket python

Crie um servidor Python Flask com flask_socketio e sirva um websocket com um topico "/topic/greetings"

com o endpoint "/gs-guide-websocket". 
o servidor websocket deve rodar na porta 5011

Esse serviço deve enviar a cada 2 segundos uma mensagem json para os inscritos no topico "/topic/greetings" com o seguinte formato JSON:
````
{"e":"trade","E":1722766102790,"s":"BTCUSDT","t":3718209179,"p":"60610.00000000","q":"0.00154000","T":1722766102789,"m":true,"M":true}
````

# VERSAO BITCVOIN
Crie um servidor Python Flask com flask_socketio e sirva um websocket com o endpoint "/ws". 
o servidor websocket deve rodar na porta 5011


Esse serviço deve enviar a cada 2 segundos uma mensagem json broadcast com o valor do bitcoin que foi recuperado na api 'https://api.coinbase.com/v2/prices/btc-usd/spot'. 




## P2
crie um programa Python cliente que vai se conectar em um servidor flash  de websocket, fique ouvindo os eventos de um topico "/topic/greetings"

no endpoint "/gs-guide-websocket" que esta rodando em localhost na porta 5011 e esta enviando um objeto json seguinte formato :
````
{"e":"trade","E":1722766102790,"s":"BTCUSDT","t":3718209179,"p":"60610.00000000","q":"0.00154000","T":1722766102789,"m":true,"M":true}
````
# SUBIR CONTAINER LOCAL
docker run --name fabao-socket-server -p 80:80 fabioalvaro/socketserver:latest

# P3 
Como configurar o postman para ouvir os eventos de um topico "/topic/greetings" no servidor websocket que esta rodando em localhost na porta 5011

# instale  os pacotes
$ virtualenv poc
$ poc/bin/activate
$ pip install --upgrade pip
$ pip install websockets flask flask_socketio requests pip install gevent gevent-websocket

# OUVIR OS EVENTOS
$ npm install -g wscat
$ wscat -c ws://localhost:5011/gs-guide-websocket
$ wscat -c http://192.168.1.104:5011/gs-guide-websocket
$ websocat ws://localhost:5011/gs-guide-websocket
$ websocat http://192.168.1.104:5011/gs-guide-websocket
$ websocat ws://127.0.0.1:5011/gs-guide-websocket