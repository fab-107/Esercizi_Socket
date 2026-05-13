import socket
import time


HOST = "127.0.0.1"
PORT = 65432
NUM_PINGS = 5
PAUSA = 0.5
BUFFER_SIZE = 1024


def crea_socket_client():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    print(f"[Client] Connesso a {HOST}:{PORT}")
    return client_sock


def invia_ping(client_sock, numero):
    message = "PING"
    print(f"\n[Client] Invio #{numero}: {message!r}")

    try:
        client_sock.sendall(message.encode("utf-8"))
        data = client_sock.recv(BUFFER_SIZE)
        reply = data.decode("utf-8")
        print(f"[Client] Risposta:  {reply!r}")

    except OSError as e:
        print(f"[Client] Errore durante il ping #{numero}: {e}")


def esegui_sessione(client_sock):
    for i in range(1, NUM_PINGS + 1):
        invia_ping(client_sock, i)
        time.sleep(PAUSA)


def main():
    client_sock = crea_socket_client()

    try:
        esegui_sessione(client_sock)

    finally:
        print("\n[Client] Tutti i ping inviati. Chiusura connessione.")
        client_sock.close()


if __name__ == "__main__":
    main()
