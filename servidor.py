import socket
import threading


# Semáforo para controlar o acesso concorrente à agenda
semaforo = threading.Semaphore()


# Função para lidar com cada cliente em uma thread separada
def handle_client(cliente_socket):
    while True:
        # Recebe uma requisição do cliente através do socket 
        # e decodifica de bytes para string usando UTF-8
        requisicao = cliente_socket.recv(1024).decode("utf-8")

        if not requisicao:
            break

        # Tratamento das opções do cliente
        if requisicao == "1":
            adicionar_contato(cliente_socket)
        elif requisicao == "2":
            exibir_lista(cliente_socket)
        elif requisicao == "3":
            excluir_contato(cliente_socket)
        elif requisicao == "4":
            break
        else:
            cliente_socket.send("Opção inválida. Tente novamente.".encode("utf-8"))

    cliente_socket.close()


# Função para adicionar um contato à agenda
def adicionar_contato(cliente_socket):
    global semaforo
    with semaforo:
        nome = cliente_socket.recv(1024).decode("utf-8")
        telefone = cliente_socket.recv(1024).decode("utf-8")

        contato = f"{nome}: {telefone}\n"

        with open("agenda.txt", "a") as arquivo:
            arquivo.write(contato)

        cliente_socket.send(f"Contato {nome} adicionado com sucesso!".encode("utf-8"))
    semaforo.release()


# Função para exibir a lista de contatos da agenda
def exibir_lista(cliente_socket):
    global semaforo
    with semaforo:
        with open("agenda.txt", "r") as arquivo:
            lista_contatos = arquivo.readlines()

        if lista_contatos:
            contatos_str = "\n".join(lista_contatos)
            cliente_socket.send(contatos_str.encode("utf-8"))
        else:
            cliente_socket.send("A agenda está vazia.".encode("utf-8"))
    semaforo.release()


# Função para excluir um contato da agenda
def excluir_contato(cliente_socket):
    global semaforo
    with semaforo:
        nome = cliente_socket.recv(1024).decode("utf-8")

        with open("agenda.txt", "r") as arquivo:
            lista_contatos = arquivo.readlines()

        with open("agenda.txt", "w") as arquivo:
            excluido = False
            for contato in lista_contatos:
                if nome.lower() not in contato.lower():
                    arquivo.write(contato)
                else:
                    excluido = True
            
            if excluido:
                cliente_socket.send(f"Contato {nome} excluído com sucesso!".encode("utf-8"))
            else:
                cliente_socket.send(f"Contato {nome} não encontrado.".encode("utf-8"))
    semaforo.release()


# Função principal que inicia o servidor e aguarda conexões
def main():
    # Cria um socket / AF_INET indica endereço IPV4 e 
    # SOCK.STREAM indica que é um socket TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associa o socket do servidor a um endereço(IP) 
    # e porta específicos
    servidor.bind(('127.0.0.1', 8080))
    # Listen habilita o socket do servidor para aceitar apenas 5 conexões
    servidor.listen(5)

    print("[*] Aguardando conexões...")

    while True:
        cliente, endereco = servidor.accept()
        print(f"[*] Conexão aceita de {endereco[0]}:{endereco[1]}")

        novo_cliente = threading.Thread(target=handle_client, args=(cliente,))
        novo_cliente.start()

if __name__ == "__main__":
    main()
