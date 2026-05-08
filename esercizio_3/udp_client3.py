import socket
import time

HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024
TIMEOUT = 2.0
NUM_PINGS = 5
PAUSA = 0.5

def crea_socket_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    return sock

def invia_ping(sock, numero):
    message = "PING"
    print(f"[Client] Invio #{numero}: {message!r}")
    sock.sendto(message.encode("utf-8"), (HOST, PORT))

    try:
        data, server_addr = sock.recvfrom(BUFFER_SIZE)
        reply = data.decode("utf-8")
        print(f"[Client] Risposta da {server_addr}: {reply!r}\n")
    except socket.timeout:
        print(f"[Client] Timeout! Il server non ha risposto al ping #{numero}. Passo al prossimo...\n")

def esegui_sessione(sock):
    for i in range(1, NUM_PINGS + 1):
        invia_ping(sock, i)
        time.sleep(PAUSA)

def main():
    sock = crea_socket_client()
    try:
        esegui_sessione(sock)
    finally:
        print("[Client] Sessione terminata. Chiusura socket.")
        sock.close()

if __name__ == "__main__":
    main()