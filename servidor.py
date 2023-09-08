import socket
import datetime as dt
import os

class Server():
   def __init__(self):
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

      server_address = ('', 8888)
      self.server_socket.bind(server_address)

      self.comands = {'CONSULTA': self.info, 'HORA': self.hora_atual,
       'ARQUIVO': self.baixaArq, 'LISTAR': self.lista_arquivos, }

      self.dir = './dir_files_serv/'

      print('Servidor UDP pronto para receber mensagens')

   def info(self):
      return 'consulta'

   def hora_atual(self):
      horario = dt.datetime.now()
      horario = horario.strftime("%H:%M:%S")
      return str(horario)

   def baixaArq(self, nomeArq):
      try:
         with open(os.path.join(self.dir, nomeArq), 'rb') as file:
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

   def escuta(self):
      message, client_address = self.server_socket.recvfrom(1024)
      return message.decode(), client_address

   def processa(self, message):
      comand = message.split(maxsplit=1)[0]

      if len(message.split(maxsplit=1)) == 2:
         nomeArq = message.split(maxsplit=1)[1]
      else:
         nomeArq = None

      if comand not in self.comands:
         return 'o comando nao existe'.encode()
      else:

         if nomeArq:
            message_resposta = self.comands[comand](nomeArq)
         else:
            message_resposta = self.comands[comand]()

         if isinstance(message_resposta, list):
            return '\n'.join(message_resposta).encode()

         elif isinstance(message_resposta, bytes):
            return message_resposta
         
         else:
            return message_resposta.encode()

   def responde(self, message_resposta, client_address):
      self.server_socket.sendto(message_resposta, client_address)

   def run(self):
      message, client_address = self.escuta()
      message_resposta = self.processa(message)
      self.responde(message_resposta, client_address)

servidor = Server()
while True:
   servidor.run()



