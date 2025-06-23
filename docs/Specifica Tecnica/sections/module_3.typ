== Modulo 3 - Analisi dell'impatto delle modifiche

#figure(
    image("..\..\assets\commit_impact_module.png", width: 90%),
    caption: "Diagramma logico dell'architettura del software"
)

=== Struttura e responsabilità

Il modulo per l’analisi dell’impatto delle modifiche è incentrato sulla classe `CommitImpactHandler`, che si 
occupa di orchestrare l’intero flusso di raccolta dati, interazione con il modello LLM e restituzione del 
risultato all’utente.  
La classe mantiene i riferimenti ai componenti principali necessari: il percorso del file da analizzare 
(`_file_path`), il client LLM (`_llm_client`), la sessione conversazionale (`_chat_session`) e l’interfaccia 
utente (`_user_io`).

Un aspetto centrale di questo modulo è la raccolta e la preparazione dei dati necessari all’analisi. 
`CommitImpactHandler` utilizza direttamente alcune funzioni di utilità definite nel modulo `git_repository` 
(evidenziato come `«utility»` nell’UML), tra cui:
- `get_remote_head_hash(repo_path: str)`: per ottenere l’hash della testa remota del repository.
- `get_file_annotate(commit_hash: str, file_path: Path, repo_path: str)`: per recuperare le annotazioni 
(blame) di un file a uno specifico commit.
- `get_file_from_hash(commit_hash: str, file_path: Path, repo_path: str)`: per ottenere il contenuto di un 
file a uno specifico commit.

Queste funzioni non appartengono a una classe, ma sono funzioni di modulo importate e utilizzate 
direttamente da `CommitImpactHandler` per raccogliere tutte le informazioni necessarie a descrivere 
le modifiche e il loro contesto.

Il risultato dell’analisi è rappresentato dalla classe `ImpactAnalisys`, che funge da semplice contenitore 
per la risposta generata dal modello LLM (testo dell’analisi e rating numerico).

=== Pattern utilizzati

In questo modulo non sono stati adottati pattern di progettazione specifici oltre alla separazione delle 
responsabilità e alla modularizzazione del codice.

=== Estendibilità

Sebbene il modulo non sia stato progettato esplicitamente per una facile estensione, la struttura attuale 
permette di aggiungere nuove funzioni di raccolta dati o di modificare la logica di analisi senza impattare 
significativamente il resto del sistema. L’uso di funzioni di utilità esterne facilita l’integrazione di 
nuove fonti di dati o metriche di analisi, qualora necessario.

=== Sintesi del flusso

1. L’utente avvia la richiesta di analisi dell’impatto tramite CLI.
2. `CommitImpactHandler` raccoglie i dati necessari utilizzando le funzioni di utilità di `git_repository` 
(recupero hash, blame, contenuto file).
3. I dati raccolti vengono formattati e inseriti nella sessione conversazionale (`ChatSession`).
4. Il client LLM elabora la richiesta e restituisce una risposta strutturata (`ImpactAnalisys`).
5. Il risultato viene presentato all’utente.
