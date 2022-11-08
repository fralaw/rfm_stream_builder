## RFM Stream Builder


Per installare le dipendenze utilizzare il comando: ``pip install -r /path/to/requirements.txt``.

La serializzazione degli esempi etichettati avviene all'interno della cartella output e sono denominati con la data del giorno in cui sono stati etichettati.
Prima di eseguire il programma, tuttavia, è opportuno svuotare la cartella output dai risultati di eventuali precedenti esecuzioni.

Per eseguire il software è necessario utilizzare il terminale posizionandosi nella cartella 'src' del progetto e 
digitare:

``python StreamBuilder.py`` seguito dai parametri di input:
* -h, --help &emsp; show this help message and exit
* --host HOST &emsp; Il nome del server o l'indirizzo IP su cui è in esecuzione MySQL. Se si esegue su localhost è possibile utilizzare localhost o IP 127.0.0.0.
* --user USER &emsp; Il nome utente che si utilizza per lavorare con MySQL. Il nome utente predefinito per il database MySQL è root.
* --password PASSWORD &emsp; La password viene fornita dall'utente al momento dell'installazione del server MySQL.
* --database DATABASE &emsp; Il nome del database a cui si desidera connettersi ed eseguire le operazioni.
* --churnDim CHURNDIM &emsp; Dimensione del churn, di tipo int.
* --periodDim PERIODDIM &emsp; Dimensione del periodo, di tipo int.
* --periods PERIODS &emsp; Numero di periodi, di tipo int.
* --start START &emsp; Data di partenza in formato: AAAA-MM-DD, OPZIONALE: di default la prima del db.
* --end END &emsp; Data di fine in formato: AAAA-MM-DD, OPZIONALE: di default l'ultima del db.

Esempio di input:

``python StreamBuilder.py --password "la_tua_password" --database "nome_db" --churnDim 4 --periodDim 4 --periods 4 --start 2022-01-01 --end 2022-02-07``

