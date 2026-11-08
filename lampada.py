import pika
import json
import sys

print("Configuração da Lâmpada")
luminosidade_padrao = float(input("Defina a luminosidade padrão (lux) a ser armazenada: "))
print("Valor armazenado com sucesso!!\n")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
except Exception as e:
    print("Erro ao conectar no RabbitMQ.")
    sys.exit(1)

channel.exchange_declare(exchange='iluminacao', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='iluminacao', queue=queue_name)

def callback(ch, method, properties, body):
    dados = json.loads(body)
    lux = dados.get("lux")
    
    print(f"\n[x] Leitura do sensor: {lux} lux")
    
    if lux < luminosidade_padrao:
        print("AÇÃO: Lâmpada do poste ATIVADA.")
    else:
        print("AÇÃO: Não precisa ser ajustado.")

print('Lâmpada aguardando dados de luminosidade. Pressione CTRL+C para sair.')
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nEncerrando a Lâmpada.")
    connection.close()