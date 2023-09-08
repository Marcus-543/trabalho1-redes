import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# configura o endereço IP e a porta do servidor
server_address = ('', 8888)
server_socket.bind(server_address)

print('Servidor UDP pronto para receber mensagens')

while True:
    # aguarda a chegada de uma mensagem do cliente
    messagem, client_address = server_socket.recvfrom(1024)

    # exibe a mensagem recebida
    print('Mensagem recebida:', messagem.decode())
    message_resposta = messagem.decode().upper()

    # envia uma resposta para o cliente
    server_socket.sendto(message_resposta.encode(), client_address)
    print('Mensagem recebida:', message_resposta.encode())
