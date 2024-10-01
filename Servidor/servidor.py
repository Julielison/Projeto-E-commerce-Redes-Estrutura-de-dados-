import threading
import socket
from protocolo import Protocolo
from Estoque.estoque import Estoque


class Servidor:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55550
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start (self): # Inicia o servidor
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Servidor executando na porta: ', self.port)
        while True:
            conn, addr = self.socket.accept()
            print('Conectado a', addr)
            threading.Thread(target=self.handle_client, args=(conn,)).start()
            

    def handle_client(self, conn): # Trata a conexão com o cliente e executa os comandos recebidos do cliente(Cria uma thread para cada cliente)

        while True:
            data = conn.recv(1024)
            data = data.decode()
            print('Recebido:', data)

            corpo_entidade = None
            dados_separados = data.split()
            método = dados_separados[0]
        
            if len(dados_separados) > 1:
                corpo_entidade = dados_separados[1]

            if método == 'SAIR':
                break

            resultado = processar_requisição(método, corpo_entidade)

            conn.sendall(resultado.encode())
        conn.close()


        def processar_requisição(método: str, corpo_entidade: str) -> str:
            try:
                processar_no_estoque = Protocolo.mapear_função(método)
                if corpo_entidade != None:
                    resultado = processar_no_estoque(corpo_entidade)
                else:
                    resultado = processar_no_estoque()
            except Exception as e:
                print(e)
            return resultado


if __name__ == '__main__':
    servidor = Servidor()
    servidor.start()
    estoque = Estoque()
    estoque.preencher()
    Protocolo.criar(estoque)