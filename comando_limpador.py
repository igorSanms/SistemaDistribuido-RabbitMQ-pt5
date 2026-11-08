import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='limpeza', exchange_type='fanout')

print("Controle do Limpador de Ruas")
comando = input("Digite o comando (LIGA / DESLIGA): ").strip().upper()

channel.basic_publish(exchange='limpeza', routing_key='', body=comando)
print(f"Comando enviado para a rede: {comando}")

connection.close()