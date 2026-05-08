"""
UDP Server — Ping Pong (Esercizio 1: contatore messaggi)

Autori  : [I tuoi nomi]
Data    : 2026
Versione: 3.0

Modifiche rispetto all'Esercizio 0:
  - Aggiunta variabile contatore 'ping_count' in main() e passata
    come parametro a gestisci_datagramma()
  - La funzione costruisci_risposta() ora riceve il contatore
    e restituisce "PONG #N" invece di "PONG"
  - Il contatore viene resettato a 0 ogni volta che il server
    viene riavviato (vedi nota sotto)

NOTA sul contatore:
  La variabile ping_count vive in memoria RAM. Se il server viene
  riavviato mentre il client sta girando, il contatore riparte da 1.
  Il client non si accorge del riavvio: continua a mandare PING
  ma vedrà il contatore ricominciare da capo.
"""

import socket

HOST        = "127.0.0.1"
PORT        = 65433
BUFFER_SIZE = 1024


def crea_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto per datagrammi UDP su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def costruisci_risposta(message, contatore):
    """
    Costruisce la risposta includendo il contatore nel messaggio.
    
    Se il messaggio è PING restituisce "PONG #N" dove N è il numero
    di PING ricevuti fino a questo momento.
    Il contatore è passato come parametro: la funzione non ha effetti
    collaterali e rimane testabile in modo isolato.
    """
    if message == "PING":
        return f"PONG #{contatore}"   # es. "PONG #1", "PONG #2" ...
    return f"Sconosciuto: {message!r}"


def gestisci_datagramma(sock, contatore):
    """
    Riceve un datagramma, incrementa il contatore e invia la risposta.
    
    Il contatore viene passato dall'esterno (da main) e restituito
    aggiornato: questo evita di usare variabili globali.
    """
    data, client_addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8").strip()
    print(f"[Server] Ricevuto {message!r} da {client_addr}")

    # Incrementa il contatore solo se il messaggio è PING
    if message == "PING":
        contatore += 1

    reply = costruisci_risposta(message, contatore)

    sock.sendto(reply.encode("utf-8"), client_addr)
    print(f"[Server] Inviato {reply!r} a {client_addr}\n")

    # Restituisce il contatore aggiornato a main()
    return contatore


def main():
    sock = crea_socket_server()
    # Il contatore parte da 0 e viene aggiornato ad ogni PING ricevuto.
    # Vive in memoria: se il server si riavvia riparte da 0.
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