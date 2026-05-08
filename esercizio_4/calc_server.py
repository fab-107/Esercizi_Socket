import socket
 
HOST        = "127.0.0.1"
PORT        = 65435
BUFFER_SIZE = 1024
MAX_CLIENTS = 5
 
 
def crea_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(MAX_CLIENTS)
    print(f"[Server] Calcolatrice in ascolto su {HOST}:{PORT}")
    return sock
 
 
def calcola(espressione):
    operatori_consentiti = set("0123456789+-*/(). ")
    if not all(c in operatori_consentiti for c in espressione):
        return "ERRORE: espressione non valida"
    try:
        risultato = eval(espressione)
        return f"Risultato: {risultato}"
    except:
        return "ERRORE: espressione non valida"
 
 
def gestisci_client(conn, addr):
    print(f"[Server] Client connesso: {addr}")
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            messaggio = data.decode("utf-8").strip()
            print(f"[Server] Ricevuto da {addr}: {messaggio!r}")
            if messaggio.upper() == "EXIT":
                print(f"[Server] Client {addr} ha chiuso la sessione.")
                break
            risposta = calcola(messaggio)
            conn.sendall(risposta.encode("utf-8"))
            print(f"[Server] Risposta inviata: {risposta!r}")
    except OSError:
        pass
    finally:
        conn.close()
 
 
def main():
    sock = crea_socket_server()
    try:
        while True:
            conn, addr = sock.accept()
            gestisci_client(conn, addr)
    except KeyboardInterrupt:
        print("\n[Server] Chiusura in corso...")
    finally:
        sock.close()
 
 
if __name__ == "__main__":
    main()