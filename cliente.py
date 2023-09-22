import socket
import os

class Cliente(object):
    def __init__(self):
       self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
       self.server_address = ('localhost', 8888)
       self.client_socket.connect(self.server_address)
       
       self.comands = [
        'CONSULTA: solicita informaçoes do servidor', 
        'HORA: informa a hora atual do servidor',
        'ARQUIVO nome_do_arquivo: baixa arquivo especificado',
        'LISTAR: lista todos os arquivos disponiveis',
        'SAIR: encerra a conexão com o servidor'
        ]
       self.dir = 'dir_files_cli'
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
        self.client_socket.send(str.encode(message_enviada))

    def res(self):
        message_recebida = self.client_socket.recv(1024)

        if (message_recebida.decode() != 'FileNotFound' and message_recebida.decode() != 'ComandNotFound') and self.nomeArq:
            with open(os.path.join(self.dir, self.nomeArq), 'wb') as arq: #wb
                arq.write(message_recebida)
            print('arquivo baixado')

        else:
            if message_recebida.decode() == 'FileNotFound':
                print('Arquivo informado nao existe')
            elif message_recebida.decode() == 'ComandNotFound':
                print('Comando informado nao existe')
            elif message_recebida.decode() == 'Adeus':
                print(message_recebida.decode())
                return False
            else:
                print(message_recebida.decode())

        print('--------------------------------------------------------------------')

    def run(self):
        while True:
            self.menu()
            self.req()
            if self.res() == False:
                break

cliente = Cliente()
cliente.run()
