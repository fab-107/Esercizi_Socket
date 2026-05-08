"""
UDP Server — Ping Pong (Esercizio 0: riscrittura con funzioni)

Autori  : [I tuoi nomi]
Data    : 2026
Versione: 2.0

Modifiche rispetto all'originale:
  - Il codice è stato suddiviso in funzioni separate:
      crea_socket_server()  → crea il socket UDP e lo associa alla porta
      costruisci_risposta() → logica pura di costruzione della risposta (testabile)
      gestisci_datagramma() → riceve un datagramma, costruisce e invia la risposta
      main()                → loop principale con gestione KeyboardInterrupt
  - La funzione costruisci_risposta() isola la logica di business:
    separare la logica dalla rete rende il codice più testabile
  - Le costanti HOST, PORT e BUFFER_SIZE sono definite a livello di modulo
"""

import socket


# ── Costanti di configurazione ───────────────────────────────────────────────
HOST        = "127.0.0.1"   # accetta datagrammi solo da questa macchina
PORT        = 65433          # porta diversa dal TCP per evitare conflitti
BUFFER_SIZE = 1024           # bytes massimi per datagramma (eccesso viene scartato)


def crea_socket_server():
    """
    Crea un socket UDP e lo associa all'indirizzo e alla porta configurati.

    A differenza del TCP:
      - Non c'è listen() perché UDP non ha code di connessione
      - Non c'è accept() perché UDP non stabilisce connessioni

    Restituisce il socket pronto a ricevere datagrammi.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[Server] In ascolto per datagrammi UDP su {HOST}:{PORT} ...")
    print("[Server] Premi Ctrl+C per fermare.\n")
    return sock


def costruisci_risposta(message):
    """
    Determina la risposta da inviare in base al messaggio ricevuto.

    Isolare questa logica in una funzione separata ha due vantaggi:
      1. È facilmente testabile senza aprire socket
      2. Modificare le regole del protocollo richiede di toccare solo questa funzione

    Parametri:
      message: stringa del messaggio ricevuto (già decodificata e ripulita)

    Restituisce la stringa di risposta.
    """
    if message == "PING":
        return "PONG"
    return f"Sconosciuto: {message!r}"


def gestisci_datagramma(sock):
    """
    Riceve un singolo datagramma, costruisce la risposta e la invia al mittente.

    In UDP ogni datagramma è indipendente: recvfrom() restituisce anche
    l'indirizzo del mittente perché il socket non ha memoria di sessioni precedenti.

    Parametri:
      sock: il socket UDP già in ascolto
    """
    data, client_addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode("utf-8").strip()
    print(f"[Server] Ricevuto {message!r} da {client_addr}")

    reply = costruisci_risposta(message)

    # sendto() richiede l'indirizzo di destinazione ad ogni chiamata
    # perché UDP non ha una "connessione corrente" da cui ricavarlo
    sock.sendto(reply.encode("utf-8"), client_addr)
    print(f"[Server] Inviato {reply!r} a {client_addr}\n")


def main():
    """
    Funzione principale: crea il socket e rimane in loop
    chiamando gestisci_datagramma() per ogni datagramma ricevuto.
    """
    sock = crea_socket_server()
    try:
        while True:
            gestisci_datagramma(sock)
    except KeyboardInterrupt:
        # Ctrl+C: uscita pulita senza traceback
        print("\n[Server] Fermato.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
