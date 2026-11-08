import pika
import json
import sys

print("Semáforo Inteligente")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
except Exception as e:
    print("Erro ao conectar no RabbitMQ.")
    sys.exit(1)

channel.exchange_declare(exchange='transito', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='transito', queue=queue_name)

def callback(ch, method, properties, body):
    dados = json.loads(body)
    urgencia = dados.get("urgencia")
    
    print(f"\nAlerta do sensor recebido: Veículo de urgência = {urgencia}")
    
    if urgencia:
        print("AÇÃO: Alterando fase para posição de ESPERAR (VERMELHO).")
    else:
        print("AÇÃO: Operação normal.")

print('Semáforo aguardando alertas de trânsito. Pressione CTRL+C para sair.')
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nEncerrando o Semáforo.")
    connection.close()