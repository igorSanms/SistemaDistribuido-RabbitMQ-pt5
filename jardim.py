import pika
import json
import sys

print("Configuração Inicial do Jardim")
limite_umidade = float(input("Defina o limite de umidade ideal do solo (%): "))
print("Valor armazenado com sucesso!\n")

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
except Exception as e:
    print("Erro ao conectar no RabbitMQ.")
    sys.exit(1)

channel.exchange_declare(exchange='clima', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='clima', queue=queue_name)

def callback(ch, method, properties, body):
    dados = json.loads(body)
    chuva_sensor = dados.get("chuva")
    umidade_sensor = dados.get("umidade")
    
    print(f"\nDados recebidos do sensor: Chuva={chuva_sensor}, Umidade={umidade_sensor}%")
    
    if chuva_sensor and (umidade_sensor < limite_umidade):
        print("AÇÃO: Jardim ativado e libera a chuva ao solo.")
    else:
        print("AÇÃO: Não precisa ser ajustado.")

print('Jardim aguardando dados do sensor de clima. Pressione CTRL+C para sair.')
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nEncerrando o Jardim.")
    connection.close()