# RFM Stream Builder


Per installare le dipendenze utilizzare il comando: ``pip install -r /path/to/requirements.txt``.

## Generazione stream di esempi

La serializzazione degli esempi etichettati avviene all'interno della cartella output e sono denominati con la data del giorno in cui sono stati etichettati.

**Prima di eseguire il programma, tuttavia, è opportuno svuotare la cartella output dai risultati di eventuali precedenti esecuzioni.**

Per eseguire il software è necessario utilizzare il terminale posizionandosi nella cartella 'src/streamBuilder' del progetto e 
digitare:

``python StreamBuilder.py`` seguito dai parametri di input:
* -h, --help &emsp; mostra la lista dei comandi
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

``python StreamBuilder.py --password "la_tua_password" --database "nome_db" --churnDim 115 --periodDim 60 --periods 3 --start 2022-01-01 --end 2022-02-07``

Nella cartella resources è possibile trovare il diagramma delle classi e lo scripts sql per creare un db di test.

## Addestramento e Classificazione

Dopo aver serializzato gli esempi nella cartella output, i file verranno caricati dal programma di addestramento e classificazione.

Per eseguire il software è necessario utilizzare il terminale posizionandosi nella cartella 'rfm_stream_builder' del progetto e digitare:

``python -m src.classification.online.Main`` per algoritmi di apprendimento online
oppure ``python -m src.classification.offline.Main`` per algoritmi di apprendimento offline

seguito dai parametri di input:
* --start START &emsp; Data di partenza in formato: AAAA-MM-DD, OPZIONALE: di default la prima della cartella.
* --end END &emsp; Data di fine in formato: AAAA-MM-DD, OPZIONALE: di default l'ultima della cartella.
* --serialized NAME &emsp; Parametro per caricare un modello precedentemente serializzato.

**Se vengono inseriti i parametri opzionali di start ed end è opportuno inserirli entrambi affinchè l'algoritmo funzioni correttamente.**

Si dovrà successivamente scegliere nella lista presente, il numero dell'algoritmo da testare.

Al termine del processo si potrà scegliere se serializzare il modello appena addestrato. Inoltre è possibile salvare
il nome del modello con uno inserito da input.

Il nostro programma presenta anche la funzione di caricamento del modello serializzato: basta specificare l'argomento ``--serialized``"nome_file"


