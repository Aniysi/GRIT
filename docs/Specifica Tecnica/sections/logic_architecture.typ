= Architettura Logica

L’architettura logica del software nella cartella `src` segue un approccio modulare e a livelli, ispirato ai principi della 
Clean Architecture e del Domain-Driven Design. I principali moduli individuati sono:

== 1. CLI (Interfaccia a Riga di Comando)
La cartella `cli/` contiene i punti di ingresso dell’applicazione (`main.py`), la gestione dell’input/output utente 
(`user_io.py`) e il parser dei comandi (`command_parser.py`). Questo livello si occupa esclusivamente dell’interazione con 
l’utente e della raccolta delle richieste, delegando la logica applicativa ai moduli sottostanti.

== 2. Application Layer
La cartella `application/` implementa la logica di orchestrazione delle funzionalità principali tramite handler specializzati:
- `cmd_conversation_hanlder.py`, `commit_conversation_handler.py`, `commit_impact_handler.py`, `merge_conflict_handler.py`: 
gestiscono i diversi flussi conversazionali e le operazioni core (generazione comandi, commit, analisi impatto, risoluzione 
conflitti).
- Sottocartelle come `rag/` contengono la logica per la costruzione del contesto tramite RAG (Retrieval-Augmented Generation).

== 3. Dominio
La cartella `domain/` definisce le strutture dati centrali e i prompt per l’interazione con il modello LLM:
- `chat.py`, `prompts.py`, `response_structure.py`: rappresentano le entità, i messaggi e i formati di risposta usati in tutto 
il sistema.

== 4. Infrastructure
La cartella `infrastructure/` fornisce servizi di basso livello e componenti tecnici:
- `embedding/`: pipeline di embedding, chunking e gestione RAG.
- `git_service/`: astrazioni per l’interazione con Git (diff, repository, annotazioni).
- `llm/`: client per la comunicazione con modelli LLM (es. Ollama).
- `database/`: gestione del database vettoriale per il retrieval.
- File contenente gli esempi che costituscono il corpo del sistema di RAG (`examples.json`).

== 5. Configurazione
La cartella `config/` contiene la configurazione centralizzata del sistema (`config.py`, `config.json`), permettendo la 
parametrizzazione dei modelli e delle lingue.

== 6. Scripts
La cartella `scripts/` ospita utility e script di supporto che non fanno strettamente parte del software eseguibile, ma sono stati
utilizzati nel corso della produzione di tale software.

== Relazioni tra i moduli
- Il livello CLI riceve input dall’utente e invoca gli handler dell’application layer.
- Gli handler orchestrano le operazioni, interagendo con il dominio per la gestione dei dati e con l’infrastructure per 
i servizi tecnici (Git, embedding, LLM).
- La configurazione è accessibile trasversalmente da tutti i moduli.
- L’infrastruttura è progettata per essere facilmente sostituibile o estendibile (es. nuovi modelli LLM, database, chunker).

== Diagramma logico
#figure(
    image("../../assets/logic_architecture_scheme.png", width: 50%),
    caption: "Diagramma logico dell'architettura del software"
)

Questa architettura garantisce separazione delle responsabilità, testabilità e facilità di estensione, rendendo il sistema 
robusto e manutenibile.