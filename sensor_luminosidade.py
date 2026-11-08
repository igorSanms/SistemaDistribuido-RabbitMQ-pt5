import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='iluminacao', exchange_type='fanout')

print("Simulação do Sensor de Luminosidade")
lux = float(input("Qual a luminosidade atual do ambiente (em lux): "))

mensagem = json.dumps({"lux": lux})

channel.basic_publish(exchange='iluminacao', routing_key='', body=mensagem)
print(f"Dados de luz enviados: {mensagem}")

connection.close()