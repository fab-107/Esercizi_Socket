"""
TCP Server — Ping Pong (Esercizio 0: riscrittura con funzioni)

Autori  : [I tuoi nomi]
Data    : 2026
Versione: 2.0

Modifiche rispetto all'originale:
  - Il codice è stato suddiviso in funzioni separate con responsabilità ben definite:
      crea_socket_server()  → crea e configura il socket
      avvia_ascolto()       → esegue bind + listen
      gestisci_client()     → gestisce tutta la comunicazione con un client
      main()                → orchestratore: chiama le altre funzioni in ordine
  - Aggiunto blocco try/finally nel main per garantire la chiusura del socket
    anche in caso di errore o interruzione (Ctrl+C)
  - Aggiunto blocco try/except nella gestione del client per intercettare errori
    di rete senza far crashare il server
  - Le costanti HOST, PORT e BUFFER_SIZE sono definite a livello di modulo
    per essere facilmente modificabili senza entrare nel codice
"""

import socket


# ── Costanti di configurazione ───────────────────────────────────────────────
HOST        = "127.0.0.1"   # indirizzo loopback: accetta solo connessioni locali
PORT        = 65432          # porta di ascolto (> 1024 non richiede privilegi di root)
BUFFER_SIZE = 1024           # dimensione massima del buffer di ricezione in byte


def crea_socket_server():
    """
    Crea e configura il socket TCP del server.

    Operazioni eseguite:
      1. socket.socket(AF_INET, SOCK_STREAM) → crea un socket TCP su IPv4
      2. setsockopt(SO_REUSEADDR)            → permette il riutilizzo immediato
                                               della porta dopo il riavvio del server

    Restituisce il socket configurato ma non ancora associato a nessun indirizzo.
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR evita l'errore "Address already in use" sui riavvii rapidi
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server_sock


def avvia_ascolto(server_sock):
    """
    Associa il socket all'indirizzo/porta e mette il server in ascolto.

    Parametri:
      server_sock: il socket TCP già creato e configurato

    Operazioni eseguite:
      1. bind((HOST, PORT)) → associa il socket all'interfaccia e alla porta
      2. listen(1)          → imposta la modalità passiva con backlog di 1
                              (al massimo 1 connessione in attesa nella coda del kernel)
    """
    server_sock.bind((HOST, PORT))
    server_sock.listen(1)
    print(f"[Server] In ascolto su {HOST}:{PORT} ...")


def gestisci_client(conn, addr):
    """
    Gestisce l'intera sessione di comunicazione con un singolo client.

    Parametri:
      conn: socket dedicato alla connessione con questo client (restituito da accept())
      addr: tupla (ip, porta) che identifica il client remoto

    Logica:
      - Rimane in loop leggendo messaggi finché il client non chiude la connessione
        (recv restituisce b"" quando il peer chiude il socket)
      - Risponde "PONG" a "PING", oppure segnala messaggi sconosciuti
      - In caso di errore di rete, esce dal loop pulitamente
    """
    print(f"[Server] Connessione accettata da {addr}")
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)

            # recv() restituisce b"" quando il client ha chiuso la connessione
            if not data:
                print("[Server] Il client ha chiuso la connessione.")
                break

            message = data.decode("utf-8").strip()
            print(f"[Server] Ricevuto: {message!r}")

            # Costruzione della risposta
            reply = "PONG" if message == "PING" else f"Messaggio sconosciuto: {message!r}"

            conn.sendall(reply.encode("utf-8"))
            print(f"[Server] Inviato:  {reply!r}")

    except OSError as e:
        # Errore di rete imprevisto (es. connessione interrotta bruscamente)
        print(f"[Server] Errore di rete: {e}")
    finally:
        # Il blocco finally garantisce che conn venga sempre chiuso,
        # sia in caso di uscita normale dal loop sia in caso di eccezione
        conn.close()
        print(f"[Server] Connessione con {addr} chiusa.")


def main():
    """
    Funzione principale: crea il socket, avvia l'ascolto, accetta un client
    e gestisce la comunicazione. Chiude il server socket alla fine.
    """
    server_sock = crea_socket_server()
    try:
        avvia_ascolto(server_sock)
        conn, addr = server_sock.accept()
        gestisci_client(conn, addr)
    finally:
        # Chiude il socket di ascolto in ogni caso (anche con Ctrl+C)
        server_sock.close()
        print("[Server] Socket del server chiuso.")


if __name__ == "__main__":
    main()
