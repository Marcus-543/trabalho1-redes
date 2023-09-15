import socket
import datetime as dt
import os
import threading

class Server():
   def __init__(self):
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      server_address = ('', 8888)
      self.server_socket.bind(server_address)

      self.comands = {'CONSULTA': self.info, 'HORA': self.hora_atual,
       'ARQUIVO': self.baixaArq, 'LISTAR': self.lista_arquivos, }

      self.dir = 'dir_files_serv'

      print('Servidor TCP pronto para receber mensagens')

   def info(self):
      return 'consulta'

   def hora_atual(self):
      horario = dt.datetime.now()
      horario = horario.strftime("%H:%M:%S")
      return str(horario)

   def baixaArq(self, nomeArq):
      try:
         with open(os.path.join(self.dir, nomeArq), 'r') as file: #rb
            arq = file.read()
         return arq
      except FileNotFoundError:
         return 'o arquivo nao existe ou seu nome nao foi informado'
      except Exception as e:
         return str(e)

   def lista_arquivos(self):
      try:
         arqs = os.listdir(self.dir)
         if arqs:
            return arqs
         else:
            return 'nenhum arquivo disponível'
      except Exception as e:
         return 'erro ao listar arquivos: '+str(e)


   def escuta(self, client_socket, client_adress):
      print(f'conectado a {client_adress}')
      message = client_socket.recv(1024)
      message_resposta = self.processa(message)
      #message_resposta = message_resposta.encode() #erro no encode
      
      client_socket.send(message_resposta)
      client_socket.close()

   def processa(self, message):
      command = message.split(maxsplit=1)[0]

      if len(message.split(maxsplit=1)) == 2: 
         nomeArq = message.split(maxsplit=1)[1]
      else:
         nomeArq = None

      if command not in self.comands:
         return 'o comando nao existe'.encode()
      else:

         if nomeArq:
            message_resposta = self.comands[command](nomeArq)
         else:
            message_resposta = self.comands[command]()

         if isinstance(message_resposta, list):
            return '\n'.join(message_resposta).encode()

         elif isinstance(message_resposta, bytes):
            return message_resposta
         
         else:
            return message_resposta.encode()

   def responde(self, message_resposta):
      self.server_socket.send(message_resposta)

   def run(self):
      self.server_socket.listen()
      while True:
         client_socket, client_address = self.server_socket.accept()
         client_thread = threading.Thread(target=self.escuta, args=(client_socket, client_address))
         client_thread.start()
         

servidor = Server()
while True:
   servidor.run()



