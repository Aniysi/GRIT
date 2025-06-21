== Modulo 2 – Generazione di messaggi di commit

=== Struttura e responsabilità

Il modulo per la generazione dei messaggi di commit è centrato sulla classe `CommitConversationHandler`, 
che svolge il ruolo di orchestratore del flusso conversazionale. Essa riceve l’input utente tramite 
`UserIO`, mantiene lo stato della conversazione (`ChatSession`) e utilizza il parser (`CLICommandParser`) 
per interpretare i comandi.  
L’interazione con il modello LLM avviene tramite l’interfaccia `LLMClient`, la cui implementazione 
concreta (`OllamaClient`) si occupa di generare la risposta (`LLMResponse`).  
La risposta del modello può essere di due tipi, distinti dal campo `mode`:  
- *COMMIT:* contiene un oggetto `CommitMsg` con titolo e corpo del messaggio di commit generato.
- *QUESTION:* contiene una lista di domande (`Questions`) che il sistema pone all’utente per chiarire o 
arricchire il contesto prima di generare il messaggio di commit definitivo.

La gestione delle azioni conseguenti al comando è affidata a una gerarchia di handler che estendono 
`CommandHandler`, tra cui `CommitHandler` e `RefineCommitHandler`, responsabili rispettivamente della 
generazione e della raffinazione dei messaggi di commit.

#figure(
    image("..\..\assets\create_commit_module.png", width: 90%),
    caption: "Diagramma logico dell'architettura del software"
)

=== Pattern utilizzati

- *Command Pattern:* ogni tipo di comando (commit, refine, quit, ecc.) è gestito da un handler dedicato 
che implementa una logica specifica, facilitando la separazione delle responsabilità e l’estendibilità 
del sistema.

=== Estendibilità

La struttura modulare consente di aggiungere facilmente nuovi tipi di handler per gestire ulteriori 
modalità di interazione o nuove tipologie di comandi, senza modificare la logica esistente. La separazione 
tra orchestratore, parser, handler e interfaccia verso il modello LLM garantisce una facile manutenibilità 
e possibilità di evoluzione del modulo.

=== Sintesi del flusso

1. L’utente inserisce un comando che avvia la generazione del messaggio di commit tramite CLI.
2. `CommitConversationHandler` raccoglie l’input, aggiorna la sessione e lo passa al parser.
3. Il comando viene interpretato e gestito dall’handler appropriato (`CommitHandler`, `RefineCommitHandler`, ecc.).
4. Il `CommitConversationHandler` interagisce con il modello LLM per generare una risposta (`LLMResponse`).
5. Se la risposta è di tipo _COMMIT_, viene proposto un messaggio di commit all’utente.
6. Se la risposta è di tipo _QUESTION_, vengono poste domande di chiarimento all’utente e il ciclo riprende fino a ottenere tutte le informazioni necessarie.
7. Il risultato finale viene restituito all’utente tramite `UserIO`.
