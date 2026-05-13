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


def costruisci_risposta(message, contatore):
    if message == "PING":
        return f"PONG #{contatore}"
    return f"Sconosciuto: {message!r}"


def gestisci_datagramma(sock, contatore):
    data, client_addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8").strip()
    print(f"[Server] Ricevuto {message!r} da {client_addr}")

    if message == "PING":
        contatore += 1

    reply = costruisci_risposta(message, contatore)

    sock.sendto(reply.encode("utf-8"), client_addr)
    print(f"[Server] Inviato {reply!r} a {client_addr}\n")

    return contatore


def main():
    sock = crea_socket_server()
    ping_count = 0

    try:
        while True:
            ping_count = gestisci_datagramma(sock, ping_count)

    except KeyboardInterrupt:
        print("\n[Server] Fermato.")
        print(f"[Server] Totale PING ricevuti: {ping_count}")

    finally:
        sock.close()


if __name__ == "__main__":
    main()
