import socket
import os

class Cliente(object):
    def __init__(self):
       self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
       self.server_address = ('localhost', 8888)
       self.comands = [
        'CONSULTA: solicita informaçoes do servidor', 
        'HORA: informa a hora atual do servidor',
        'ARQUIVO nome_do_arquivo: baixa arquivo especificado',
        'LISTAR: lista todos os arquivos disponiveis',
        ]
       self.dir = 'dir_files_cli/'
       self.nomeArq = ''

    def menu(self):
        count=1
        for comand in self.comands:
            print(str(count)+' - '+comand)
            count=count+1

    def req(self):
        message_enviada = input("Digite um comando: ")
        if len(message_enviada.split(maxsplit=1)) == 2:
            self.nomeArq = message_enviada.split(maxsplit=1)[1]
        else:
            self.nomeArq = None
        self.client_socket.sendto(str.encode(message_enviada), self.server_address)

    def res(self):
        message_recebida, endereco_ip_servidor = self.client_socket.recvfrom(2048)

        if self.nomeArq:
            with open(os.path.join(self.dir, self.nomeArq), 'wb') as arq:
                arq.write(message_recebida)
            print('arquivo baixado')

        else:
            print(message_recebida.decode())

        print('--------------------------------------------------------------------')

    def run(self):
        while True:
            self.menu()
            self.req()
            self.res()

cliente = Cliente()
cliente.run()
