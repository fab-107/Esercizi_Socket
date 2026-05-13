import socket


HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024


def crea_socket_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server_sock


def avvia_ascolto(server_sock):
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    print(f"[Server] In ascolto su {HOST}:{PORT} ...")


def gestisci_client(conn, addr):
    print(f"[Server] Connessione accettata da {addr}")

    try:
        while True:
            data = conn.recv(BUFFER_SIZE)

            if not data:
                print("[Server] Il client ha chiuso la connessione.")
                break

            message = data.decode("utf-8").strip()
            print(f"[Server] Ricevuto: {message!r}")

            reply = "PONG" if message == "PING" else f"Messaggio sconosciuto: {message!r}"

            conn.sendall(reply.encode("utf-8"))
            print(f"[Server] Inviato:  {reply!r}")

    except OSError as e:
        print(f"[Server] Errore di rete: {e}")

    finally:
        conn.close()
        print(f"[Server] Connessione con {addr} chiusa.")


def main():
    server_sock = crea_socket_server()

    try:
        avvia_ascolto(server_sock)
        conn, addr = server_sock.accept()
        gestisci_client(conn, addr)

    finally:
        server_sock.close()
        print("[Server] Socket del server chiuso.")


if __name__ == "__main__":
    main()
