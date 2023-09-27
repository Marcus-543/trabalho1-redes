import socket
import datetime as dt
import os
import threading
import platform
import psutil

class Server():
   def __init__(self):
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      server_address = ('localhost', 8888)
      self.server_socket.bind(server_address)

      self.comands = {'CONSULTA': self.info, 'HORA': self.hora_atual,
       'ARQUIVO': self.baixaArq, 'LISTAR': self.lista_arquivos, 'SAIR': self.encerrar}

      self.dir = 'dir_files_serv'

      print('Servidor TCP pronto para receber mensagens.')

   def info(self):
      info_sistema = {
         'Sistema operacional do servidor': platform.system(),
         'Versão do Sistema': platform.version(),
         'Arquitetura do Sistema': platform.architecture(),
         'CPU': platform.processor(),
         'Memória Total (GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2),
      }
      info_f = "\n".join([f"{chave}: {valor}" for chave, valor in info_sistema.items()])
      return info_f.encode()

   def hora_atual(self):
      try:
         horario = dt.datetime.now()
         horario = horario.strftime("%H:%M:%S")
         return str(horario)
      except Exception as e:
         return 'erro ao consultar horario: '+str(e)

   def baixaArq(self, nomeArq):
      try:
         arquivo_path = os.path.join(self.dir, nomeArq)
         if os.path.isfile(arquivo_path):
            with open(arquivo_path, 'rb') as file:
               arq = file.read()
            return arq
         else:
            return 'FileNotFound'
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

   def encerrar(self, client_socket):
      try:
         return 'Adeus'
         client_socket.close()
      except Exception as e:
         return 'erro ao encerrar conexao: '+str(e)

   def escuta(self, client_socket, client_adress):
      print(f'conectado a {client_adress}')
      while True:
         message = client_socket.recv(1024)
         message_resposta = self.processa(message.decode(), client_socket)
         self.responde(message_resposta, client_socket)

   def processa(self, message, client_socket):
      command = message.split(maxsplit=1)[0].upper()

      if len(message.split(maxsplit=1)) == 2: 
         nomeArq = message.split(maxsplit=1)[1]
      else:
         nomeArq = None

      if command not in self.comands:
         return 'ComandNotFound'.encode()
      else:

         if nomeArq:
            message_resposta = self.comands[command](nomeArq)
         else:
            if command == 'SAIR':
               message_resposta = self.comands[command](client_socket)
            else:
               message_resposta = self.comands[command]()

         if isinstance(message_resposta, list):
            return '\n'.join(message_resposta).encode()

         elif isinstance(message_resposta, bytes):
            return message_resposta
         
         else:
            return message_resposta.encode()

   def responde(self, message_resposta, client_socket):
      client_socket.send(message_resposta)

   def run(self):
      self.server_socket.listen()
      while True:
         client_socket, client_address = self.server_socket.accept()
         client_thread = threading.Thread(target=self.escuta, args=(client_socket, client_address))
         client_thread.start()
         
servidor = Server()
while True:
   servidor.run()



