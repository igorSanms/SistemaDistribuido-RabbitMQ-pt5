import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='clima', exchange_type='fanout')

print("Simulação do Sensor de Clima")
entrada_chuva = input("Está detectando chuva agora? (s/n): ").strip().lower()
chuva = True if entrada_chuva == 's' else False
umidade = float(input("Qual a umidade do solo medida agora (%): "))

dados_sensor = {
    "chuva": chuva,
    "umidade": umidade
}
mensagem = json.dumps(dados_sensor)

channel.basic_publish(exchange='clima', routing_key='', body=mensagem)
print(f"Dados enviados para a rede: {mensagem}")

connection.close()