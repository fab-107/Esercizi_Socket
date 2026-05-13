import socket


HOST = "127.0.0.1"
PORT = 65433
BUFFER_SIZE = 1024


def crea_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto per datagrammi UDP su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def costruisci_risposta(message):
    if message == "PING":
        return "PONG"
    return f"Sconosciuto: {message!r}"


def gestisci_datagramma(sock):
    data, client_addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8").strip()
    print(f"[Server] Ricevuto {message!r} da {client_addr}")

    reply = costruisci_risposta(message)

    sock.sendto(reply.encode("utf-8"), client_addr)
    print(f"[Server] Inviato {reply!r} a {client_addr}\n")


def main():
    sock = crea_socket_server()

    try:
        while True:
            gestisci_datagramma(sock)

    except KeyboardInterrupt:
        print("\n[Server] Fermato.")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
