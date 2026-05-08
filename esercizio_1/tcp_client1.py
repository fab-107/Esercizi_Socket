"""
TCP Client — Ping Pong (Esercizio 0: riscrittura con funzioni)

Autori  : [I tuoi nomi]
Data    : 2026
Versione: 2.0

Modifiche rispetto all'originale:
  - Il codice è stato suddiviso in funzioni separate:
      crea_socket_client()  → crea il socket e si connette al server
      invia_ping()          → invia un singolo PING e riceve la risposta
      esegui_sessione()     → loop dei 5 ping
      main()                → orchestratore con gestione try/finally
  - Aggiunto blocco try/finally per garantire la chiusura del socket
    anche in caso di errore o interruzione
  - Aggiunto try/except dentro invia_ping() per gestire errori di rete
    su un singolo ping senza interrompere l'intera sessione
  - Le costanti HOST, PORT, NUM_PINGS e PAUSA sono definite a livello modulo
"""

import socket
import time


# ── Costanti di configurazione ───────────────────────────────────────────────
HOST      = "127.0.0.1"  # indirizzo del server (stessa macchina)
PORT      = 65432         # porta del server — deve coincidere con tcp_server.py
NUM_PINGS = 5             # numero di PING da inviare
PAUSA     = 0.5           # secondi di attesa tra un ping e il successivo
BUFFER_SIZE = 1024        # dimensione massima del buffer di ricezione


def crea_socket_client():
    """
    Crea un socket TCP e stabilisce la connessione con il server.

    Esegue il three-way handshake TCP:
      SYN → SYN-ACK → ACK

    Restituisce il socket connesso.
    """
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    print(f"[Client] Connesso a {HOST}:{PORT}")
    return client_sock


def invia_ping(client_sock, numero):
    """
    Invia un singolo messaggio PING al server e stampa la risposta ricevuta.

    Parametri:
      client_sock: il socket TCP già connesso
      numero     : numero progressivo del ping (usato solo per il log)
    """
    message = "PING"
    print(f"\n[Client] Invio #{numero}: {message!r}")

    try:
        # sendall() garantisce l'invio di tutti i byte anche se l'OS
        # li accetta in più tranche
        client_sock.sendall(message.encode("utf-8"))

        # recv() blocca fino all'arrivo della risposta
        data = client_sock.recv(BUFFER_SIZE)
        reply = data.decode("utf-8")
        print(f"[Client] Risposta:  {reply!r}")

    except OSError as e:
        # Errore di rete su questo ping: lo logghiamo ma non interrompiamo la sessione
        print(f"[Client] Errore durante il ping #{numero}: {e}")


def esegui_sessione(client_sock):
    """
    Esegue la sequenza di NUM_PINGS ping, con una pausa di PAUSA secondi tra uno e l'altro.

    Parametri:
      client_sock: il socket TCP già connesso
    """
    for i in range(1, NUM_PINGS + 1):
        invia_ping(client_sock, i)
        time.sleep(PAUSA)


def main():
    """
    Funzione principale: crea il socket, esegue la sessione di ping
    e chiude la connessione al termine.
    """
    client_sock = crea_socket_client()
    try:
        esegui_sessione(client_sock)
    finally:
        # Il blocco finally garantisce la chiusura anche se si verifica un errore
        print("\n[Client] Tutti i ping inviati. Chiusura connessione.")
        client_sock.close()


if __name__ == "__main__":
    main()
