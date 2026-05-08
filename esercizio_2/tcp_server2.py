import socket
import threading

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 1024

def crea_socket_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server_sock

def avvia_ascolto(server_sock):
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"[Server] In ascolto su {HOST}:{PORT} ...")

def gestisci_client(conn, addr):
    print(f"[Server] Client connesso: {addr}")
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            message = data.decode("utf-8").strip()
            print(f"[Server] Da {addr}: {message!r}")
            reply = "PONG" if message == "PING" else f"Errore: {message!r}"
            conn.sendall(reply.encode("utf-8"))
    except OSError:
        pass
    finally:
        conn.close()
        print(f"[Server] Connessione con {addr} chiusa.")

def main():
    server_sock = crea_socket_server()
    try:
        avvia_ascolto(server_sock)
        while True:
            conn, addr = server_sock.accept()
            client_thread = threading.Thread(target=gestisci_client, args=(conn, addr))
            client_thread.start()
            print(f"[Server] Thread attivi: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[Server] Spegnimento in corso...")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()