# Servidor socket python

Crie um servidor pyhton websocket com um topico "/topic/greetings"

com o endpoint "/gs-guide-websocket". 

Esse servico deve enviar a cada 2 segundos uma mensagem json para os inscritos no topico com o seguinte formato JSON:
````
{"e":"trade","E":1722766102790,"s":"BTCUSDT","t":3718209179,"p":"60610.00000000","q":"0.00154000","T":1722766102789,"m":true,"M":true}
````
 
