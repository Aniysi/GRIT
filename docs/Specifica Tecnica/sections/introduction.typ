= Introduzione

== Scopo del documento

Questo documento descrive l'architettura logica e di sistema del software sviluppato nell’ambito del progetto di stage presso 
Zucchetti S.p.A., svolto dallo studente Leonardo Trolese. La Specifica Tecnica è rivolta a fornire una 
visione strutturata e dettagliata delle componenti del sistema, delle interazioni tra i moduli e delle scelte 
tecnologiche adottate. Essa costituisce un riferimento per lo sviluppo, il testing, la manutenzione e 
l’estensione futura del plugin realizzato.

== Obiettivi del progetto

L'obiettivo principale del progetto è la realizzazione di un plugin per il software Git, che introduca in quest'ultimo la
possibilità di gestire e generare testo in linguaggio naturale, in accompagnamento ad alcune delle principali funzionalità del
spoftware. Le principali features implementate dal plugin sono:

- generazione di comandi Git per CLI a partire da query in lingauggio naturale che descrivano l'intenzione dell'utente;
- generazione automatica di commenti di commit a seguito di analisi del codice modificato;
- l’analisi dell’impatto delle modifiche correnti sul repository remoto;
- utilizzo di LLM per la risoluzione automatizzata di coflitti di merge.

Le attività saranno accompagnate da sessioni di test e dalla produzione di documentazione tecnica, al fine 
di assicurare l’affidabilità e la riusabilità della soluzione finale.