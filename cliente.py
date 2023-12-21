
import socket

def menu():
    print("\n1. Adicionar Contato")
    print("2. Exibir Lista de Contatos")
    print("3. Excluir Contato")
    print("4. Sair")


def formatar_telefone(telefone):
    # Formatar o número de telefone para '(00) 0 0000-0000'
    return f'({telefone[:2]}) {telefone[2]} {telefone[3:7]}-{telefone[7:]}'


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 8080))


    while True:
        menu()
        opcao = input("Escolha uma opção (1/2/3/4): ")
        cliente.send(opcao.encode("utf-8"))

        if opcao == "1":
            nome = input("Digite o nome do contato: ")
            telefone = input("Digite o telefone com DDD (sem espaços ou caracteres especiais): ")
            telefone_formatado = formatar_telefone(telefone)
            cliente.send(nome.encode("utf-8"))
            cliente.send(telefone_formatado.encode("utf-8"))
            resposta = cliente.recv(1024).decode("utf-8")
            print(resposta)
        elif opcao == "2":
            resposta = cliente.recv(4096).decode("utf-8")
            print(resposta)
        elif opcao == "3":
            nome = input("Digite o nome do contato que deseja excluir: ")
            cliente.send(nome.encode("utf-8"))
            resposta = cliente.recv(1024).decode("utf-8")
            print(resposta)
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

    cliente.close()

if __name__ == "__main__":
    main()
