import socket

# cria um socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# configura o endereço IP e a porta do servidor
server_address = ('localhost', 8888)

# envia uma mensagem para o servidor

while True:
    mensagem_enviada = input("Digite uma mensagem: ")
    client_socket.sendto(str.encode(mensagem_enviada), server_address)
    mensagem_recebida, endereco_ip_servidor = client_socket.recvfrom(2048)
    print(mensagem_recebida.decode())
