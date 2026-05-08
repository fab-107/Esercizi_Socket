import socket
 
HOST        = "127.0.0.1"
PORT        = 65435
BUFFER_SIZE = 1024
 
 
def crea_socket_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[Client] Connesso al server {HOST}:{PORT}")
    print("[Client] Scrivi un'espressione come '3 + 5' oppure 'EXIT' per uscire.\n")
    return sock
 
 
def invia_espressione(sock, espressione):
    sock.sendall(espressione.encode("utf-8"))
    risposta = sock.recv(BUFFER_SIZE)
    print(f"[Client] {risposta.decode('utf-8')}\n")
 
 
def esegui_sessione(sock):
    while True:
        espressione = input("[Client] Inserisci espressione: ").strip()
        if not espressione:
            continue
        if espressione.upper() == "EXIT":
            sock.sendall("EXIT".encode("utf-8"))
            print("[Client] Sessione terminata.")
            break
        invia_espressione(sock, espressione)
 
 
def main():
    sock = crea_socket_client()
    try:
        esegui_sessione(sock)
    except OSError as e:
        print(f"[Client] Errore di connessione: {e}")
    finally:
        sock.close()
 
 
if __name__ == "__main__":
    main()