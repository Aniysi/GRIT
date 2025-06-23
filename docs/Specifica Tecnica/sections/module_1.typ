== Modulo 1 – Generazione ed esecuzione di comandi Git

Il modulo di generazione comandi è progettato secondo un’architettura orientata ai pattern Command e 
Adapter, con particolare attenzione all’estendibilità e alla separazione delle responsabilità.

#figure(
    image("..\..\assets\create_command_module.png", width: 90%),
    caption: "Diagramma logico dell'architettura del software"
)

=== Struttura e responsabilità

Il cuore del modulo è rappresentato dalla classe `CmdConversationHandler`, che funge da _orchestratore_: 
riceve l’input dell’utente tramite `UserIO`, costruisce il contesto necessario (con `RAGContextBuilder`), 
e delega la gestione del comando al parser (`CLICommandParser`). Quest’ultimo trasforma l’input in un 
oggetto `ParsedCLICommand`, identificando il tipo di comando richiesto.

La gestione effettiva dei comandi è affidata a una gerarchia di handler che implementano il pattern 
_Command_: la classe astratta `CommandHandler` definisce l’interfaccia comune (`handle(content, context)`), 
mentre le sottoclassi concrete (`ExecHandler`, `RegularHandler`, `RefineHandler`, `FixHandler`, `QuitHandler`) 
implementano la logica specifica per ciascun tipo di comando. Questo approccio consente di aggiungere 
facilmente nuovi tipi di comando semplicemente introducendo nuovi handler, senza modificare la logica 
esistente.

Il recupero del contesto è invece demandato alla classe `RAGContextBuilder` che attraverso l'attributo 
`_pipeline: AbstractRagPipelineBuilder`, estrae dal database gli intenti più coerenti con la query dell'utente,
andando poi a raffinare la ricerca attraverso l'applicazione, su di essi, dell'algoritmo di ranking BM25.
Nell'insieme questa componente realizza una ricerca ibrida.

==== Architettura del modulo RAG

#figure(
    image("..\..\assets\RAG_module.png", width: 90%),
    caption: "Diagramma logico dell'architettura del software"
)

Il modulo RAG (Retrieval-Augmented Generation) è un componente centrale per la costruzione del contesto semantico, utilizzato 
dalla classe `CmdConversationHandler` per recuperare esempi coerenti rispetto alla query dell’utente. Il modulo è costruito 
seguendo un pattern a catena di responsabilità (*Chain of Responsibility*), che consente l’aggiunta dinamica e componibile 
di handler per la lettura, la segmentazione (*chunking*) e l’embedding del contenuto.

La pipeline è costruita a partire da `RAGPipelineBuilder`, classe astratta che gestisce il concatenamento di `EmbeddingHandler`. Due specializzazioni sono fornite:
- `DocumentRAGPipelineBuilder`: per l’elaborazione di documenti statici (es. PDF);
- `QueryRAGPipelineBuilder`: per l’elaborazione di query in input (modulo 1).

Ogni `EmbeddingHandler` incapsula un’operazione specifica:
- `Reader`: legge e preprocessa il contenuto;
- `Chunker`: segmenta il testo in token, frasi o paragrafi;
- `Embedder`: genera embedding semantici tramite un modello configurabile (es. `"nomic-embed-text"`).

La componente di chunking composta da `BaseChunker` e sottoclassi è una versione modificata rispetto a quella offerta da _LangChain_,
e proviene dal repository GitHub associato al report tecnico [Evaluating Chunking Strategies for Retrieval](https://research.trychroma.com/evaluating-chunking)
redatto da Chroma.

La classe `RAGContextBuilder`, utilizzata dal modulo principale, istanzia internamente questa pipeline per costruire 
dinamicamente il contesto semantico sulla base della query utente.

=== Pattern utilizzati

- *Command Pattern:*  
  Ogni comando dell’utente viene incapsulato in un oggetto handler dedicato, che può essere eseguito in 
  modo indipendente. Questo favorisce l’estendibilità e la separazione delle responsabilità.

- *Adapter Pattern:*  
  L’interazione con componenti esterni o potenzialmente variabili (come il modello LLM) avviene tramite 
  interfacce astratte (`LLMClient`). Ad esempio, `OllamaClient` implementa l’interfaccia `LLMClient`, o `ChromaDBManager` che implementa `DBManager`, 
  permettendo di sostituire facilmente il backend LLM senza impattare il resto del sistema.

=== Estendibilità

L’architettura è pensata per facilitare l’aggiunta di nuove funzionalità: per supportare un nuovo tipo di 
comando, è sufficiente implementare una nuova sottoclasse di `CommandHandler` e registrarla nell’
orchestratore. Analogamente, l’uso di interfacce astratte per i servizi esterni (LLM, database, ecc.) 
permette di adattare il sistema a nuove tecnologie o provider con modifiche minime.

=== Sintesi del flusso

1. L’utente inserisce una query tramite CLI.
2. `CmdConversationHandler` raccoglie l’input, e lo passa al parser.
3. `CLICommandParser` restituisce un oggetto `ParsedCLICommand` che identifica il tipo di comando.
4. L’orchestratore seleziona l’handler appropriato e ne invoca il metodo `handle`.
5. Gli handler possono interagire con il modello LLM (tramite l’interfaccia `LLMClient`), con la pipeline di ricerca ibrida e con altri servizi secondo necessità.
6. Il risultato viene restituito all’utente tramite `UserIO`.

Questa organizzazione garantisce modularità, testabilità e facilità di evoluzione del modulo di generazione