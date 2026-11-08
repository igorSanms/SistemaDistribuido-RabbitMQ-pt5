import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='transito', exchange_type='fanout')

print("Simulação do Sensor de Trânsito")
entrada = input("Foi detectado um veículo em serviço de urgência? (s/n): ").strip().lower()
urgencia = True if entrada == 's' else False

mensagem = json.dumps({"urgencia": urgencia})

channel.basic_publish(exchange='transito', routing_key='', body=mensagem)
print(f"Alerta enviado para a rede: {mensagem}")

connection.close()