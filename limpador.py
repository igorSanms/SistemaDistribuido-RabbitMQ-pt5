import pika
import sys

print("Limpador das Ruas")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
except Exception as e:
    print("Erro ao conectar no RabbitMQ.")
    sys.exit(1)

channel.exchange_declare(exchange='limpeza', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='limpeza', queue=queue_name)

def callback(ch, method, properties, body):
    comando = body.decode()
    
    print(f"\nComando recebido: {comando}")
    
    if comando == "LIGA":
        print("AÇÃO: Realizando a limpeza do ambiente.")
    elif comando == "DESLIGA":
        print("AÇÃO: Limpeza encerrada.")
    else:
        print("AÇÃO: Comando não reconhecido.")

print('Aguardando comandos para o limpador de ruas. Pressione CTRL+C para sair.')
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nEncerrando o Limpador.")
    connection.close()