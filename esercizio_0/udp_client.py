"""
UDP Client — Ping Pong (Esercizio 0: riscrittura con funzioni)

Autori  : [I tuoi nomi]
Data    : 2026
Versione: 2.0

Modifiche rispetto all'originale:
  - Il codice è stato suddiviso in funzioni separate:
      crea_socket_client()  → crea il socket UDP con timeout
      invia_ping()          → invia un datagramma e gestisce la risposta o il timeout
      esegui_sessione()     → loop dei 5 ping
      main()                → orchestratore con try/finally
  - La gestione del timeout è incapsulata dentro invia_ping():
    ogni ping fallisce in modo isolato senza interrompere i successivi
  - Le costanti sono definite a livello di modulo per facile configurazione
"""

import socket
import time


# ── Costanti di configurazione ───────────────────────────────────────────────
HOST        = "127.0.0.1"   # indirizzo del server
PORT        = 65433          # porta del server — deve coincidere con udp_server.py
BUFFER_SIZE = 1024           # dimensione massima del buffer di ricezione
TIMEOUT     = 2.0            # secondi di attesa massima per la risposta
NUM_PINGS   = 5              # numero di PING da inviare
PAUSA       = 0.5            # secondi di pausa tra un ping e il successivo


def crea_socket_client():
    """
    Crea un socket UDP e imposta il timeout di ricezione.

    Il timeout è necessario perché UDP non garantisce la consegna:
    senza di esso recvfrom() potrebbe bloccarsi per sempre se il
    datagramma viene perso o il server non risponde.

    Restituisce il socket configurato.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    print(f"[Client] Socket UDP pronto. Invierò a {HOST}:{PORT}\n")
    return sock


def invia_ping(sock, numero):
    """
    Invia un singolo datagramma PING e gestisce la risposta o il timeout.

    A differenza del TCP:
      - sendto() richiede l'indirizzo di destinazione ad ogni chiamata
      - recvfrom() restituisce sia i dati sia l'indirizzo del mittente
      - Il try/except gestisce il caso in cui il pacchetto venga perso

    Parametri:
      sock   : socket UDP già configurato
      numero : numero progressivo del ping (solo per il log)
    """
    message = "PING"
    print(f"[Client] Invio #{numero}: {message!r}")

    # sendto() invia UN datagramma all'indirizzo specificato
    sock.sendto(message.encode("utf-8"), (HOST, PORT))

    try:
        data, server_addr = sock.recvfrom(BUFFER_SIZE)
        reply = data.decode("utf-8")
        print(f"[Client] Risposta da {server_addr}: {reply!r}")

    except socket.timeout:
        # Nessuna risposta entro TIMEOUT secondi: il datagramma potrebbe essere
        # stato perso oppure il server non è raggiungibile
        print(f"[Client] Timeout — nessuna risposta per il ping #{numero}")


def esegui_sessione(sock):
    """
    Esegue la sequenza di NUM_PINGS ping con una pausa tra uno e l'altro.

    Parametri:
      sock: il socket UDP già configurato
    """
    for i in range(1, NUM_PINGS + 1):
        invia_ping(sock, i)
        time.sleep(PAUSA)


def main():
    """
    Funzione principale: crea il socket, esegue la sessione
    e chiude il socket al termine.
    """
    sock = crea_socket_client()
    try:
        esegui_sessione(sock)
    finally:
        print("\n[Client] Fatto. Chiusura socket.")
        sock.close()


if __name__ == "__main__":
    main()
