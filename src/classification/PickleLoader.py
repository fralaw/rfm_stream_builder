"""
// Name        : PickleLoader.py
// Author      : Andrea Brunetta, Francesco Luce
// Version     : 2.0
// Description : La seguente classe si occupa di aprire la directory contenente i pickle e caricarli, restituendo
                 il prossimo elemento fino alla fine della directory. Sono parametrizzati anche lo start e l'end.
"""

import pickle
import os


def PickleLoader(folderPath: str, start: str = None, end: str = None):
    # Inserisci nella lista 'files' la lista dei file nel folderPath.
    files = os.listdir(folderPath)
    # Prova a posizionarsi in files in posizione start, se esiste! e scorre fino a fermarsi a end, se esiste!
    # La lista files partirà da start dove start rappresenta il nome in formato 'yyyy-mm-dd' e finirà ad end.
    try:
        files = files[files.index(start): files.index(end) + 1]
    except ValueError:
        print("Uno dei file di inizio o di fine non è presente all'interno della cartella")
    # Scandisce la lista di file all'interno della cartella.
    for filename in files:
        # Concatena il percorso della cartella con il nome del file.
        file_path = os.path.join(folderPath, filename)
        # Se file_path rappresenta un file (e non una dir).
        if os.path.isfile(file_path):
            # Apriamo il file.
            with open(file_path, "rb") as f:
                # Carichiamo il pickle.
                print(f)
                yield pickle.load(f)

