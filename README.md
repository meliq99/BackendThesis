# BackendThesis

## Comando para correr este proyecto

Construir el proyecto en docker: docker-compose up --build 

Aplicacion(FastApi): python -m uvicorn main:app

Para habilitar el plugging
Rabbitmq: docker exec -it rabbitmq rabbitmq-plugins enable rabbitmq_mqtt

## cliente que envia y recibe mensaje mqtt
mosquitto_sub -h localhost -p 1883 -t test/mqtt -u mqtt_user -P mqtt_password 