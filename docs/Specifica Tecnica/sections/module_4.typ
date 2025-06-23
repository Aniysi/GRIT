== Modulo 4 – Risoluzione automatica dei conflitti di merge

#figure(
    image("..\..\assets\conflict_resolution_module.png", width: 90%),
    caption: "Diagramma logico dell'architettura del software"
)

=== Struttura e responsabilità

Il modulo per la risoluzione dei conflitti di merge è incentrato sulla classe `MergeConflictHandler`, che si occupa di 
orchestrare l’intero processo di individuazione e risoluzione dei conflitti.  
Quando viene invocato, il software verifica se il percorso fornito corrisponde a una directory o a un singolo file:  
- Se è una directory, itera su tutti i file presenti per individuare quelli in stato di conflitto.
- Se è un file, si concentra esclusivamente su quello.

L’individuazione dei file in conflitto avviene tramite la funzione di utilità `get_conflicted_files(path: str)` del modulo 
`git_repository`, che restituisce la lista dei file problematici.  
Per ciascun file in conflitto, il modulo interagisce con il modello LLM (tramite `LLMClient` e la sua implementazione 
`OllamaClient`) per tentare una risoluzione automatica.  
La risposta del modello (`ConflictResolutionResponse`) può essere di due tipi, identificati dal campo `status`:
- *RESOLVED:* il conflitto è stato risolto e viene fornito il contenuto aggiornato.
- *UNRESOLVED:* il conflitto non può essere risolto automaticamente; viene fornita una spiegazione tramite il campo `reason`.

Se la risoluzione ha successo, il file viene aggiunto all’area di staging tramite la funzione utility 
`git_add_to_staging(file_path: Path, repo_path: str)`.

=== Pattern utilizzati

In questo modulo non sono stati adottati pattern di progettazione specifici oltre alla separazione delle responsabilità e alla 
modularizzazione del codice.

=== Estendibilità

Sebbene il modulo non sia stato progettato esplicitamente per una facile estensione, la struttura attuale consente di aggiungere 
nuove strategie di risoluzione o di integrare ulteriori controlli senza modificare in modo sostanziale la logica esistente.

=== Sintesi del flusso

1. L’utente avvia la procedura di risoluzione dei conflitti specificando un file o una directory.
2. `MergeConflictHandler` utilizza la funzione utility `get_conflicted_files` per individuare i file in conflitto.
3. Per ogni file individuato, viene avviata una sessione di risoluzione tramite il modello LLM.
4. Se il conflitto viene risolto (`RESOLVED`), il file aggiornato viene aggiunto all’area di staging tramite `git_add_to_staging`.
5. Se il conflitto non può essere risolto (`UNRESOLVED`), viene fornita all’utente una spiegazione del motivo.
6. Il processo si ripete per tutti i file in conflitto nella directory.