import socket

def banner_grabbing(17, port):
    try:
        # Cria uma conexão TCP com o servidor
        s = socket.socket()
        s.connect((ip, port))

        # Envie uma solicitação de teste para o servidor
        s.send(b"HEAD / HTTP/1.1\r\n\r\n")

        # Recebe a resposta do servidor
        banner = s.recv(1024)

        # Fecha a conexão
        s.close()

        return banner.decode().strip()
    except:
        return "Não foi possível conectar ao servidor"

# Exemplo de uso
banner = banner_grabbing("exemplo.com", 80)
print("Banner:", banner)
