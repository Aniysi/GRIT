# GRIT

## Introduzione

**GRIT** è un plugin per Git scritto in **Python**, pensato per semplificare l'interazione con Git attraverso l'uso del linguaggio naturale. Il plugin sfrutta le potenzialità dei **LLM (Large Language Models)** per:

- Generare comandi Git a partire da descrizioni in linguaggio naturale fornite dall’utente;
- Creare commenti di commit templatizzati, basati sulle modifiche effettivamente apportate alla codebase e su eventuali indicazioni dell’utente.

## Requisiti Tecnologici

Per il corretto funzionamento di GRIT, assicurati che il tuo sistema soddisfi i seguenti requisiti:

- **Ollama** ≥ 0.6.6  
  Richiede:
  - Modello di embedding: `nomic-embed-text`
  - Modello LLM general-purpose (esempi testati: `Qwen3` quantizzato con 4B parametri, `Gemma` con 3B)
- **Python** ≥ 3.13.0
- **Sistema operativo**: Windows 10 o superiore

## Installazione

### 1. Scarica il progetto

È sufficiente scaricare l’ultima **release** disponibile dal [repository GitHub](#) (assicurati che includa le cartelle `./src` e `./prova`).

### 2. Posiziona i file

Estrai i file in una cartella a tua scelta nel file system di Windows.

### 3. Aggiungi la directory `./src` alla variabile di ambiente **Path**

#### Metodo rapido

1. Copia il percorso della cartella `./src`;
2. Cerca **Modifica le variabili di ambiente relative al sistema** tramite la ricerca di Windows;
3. Clicca sul primo risultato per aprire il pannello **Proprietà di sistema**;
4. Nella finestra **Proprietà di sistema**, clicca su **Variabili d’ambiente...**;

<p align="center">
  <img src="./images/image.png" alt='Menù "Proprietà di sistema"' />
</p>

5. Nella sezione inferiore della finestra **Variabili d’ambiente**, seleziona la variabile `Path` e clicca su **Modifica...**;

<p align="center">
  <img src="./images/image-1.png" alt='Menù "Variabili d’ambiente"' />
</p>

6. Nella finestra **Modifica variabile d’ambiente**, clicca su **Nuovo** e incolla il percorso della cartella `./src`;

<p align="center">
  <img src="./images/image-2.png" alt='Menù "Modifica variabile d’ambiente"' />
</p>

7. Conferma le modifiche cliccando su **OK** in tutte le finestre aperte.

Il percorso è ora correttamente impostato e il plugin è pronto all’uso.

#### Metodo ddescritto nella documentazione ufficile Windows

Alternativamente è possibile aggiungere la cartella `./src` alle variabili di sistema seguendo la guida ufficiale offerta da Microsoft, e disponibile all'indirizzo <https://learn.microsoft.com/it-it/windows/powertoys/environment-variables#editremove-variable>
