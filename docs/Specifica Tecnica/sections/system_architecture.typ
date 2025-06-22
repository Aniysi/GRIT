= Architettura di Sistema

== Panoramica Generale

Il sistema descritto è un plugin progettato per assistere gli utenti nell’utilizzo avanzato di Git tramite 
un’interfaccia a riga di comando intelligente, potenziata da modelli di linguaggio (LLM) e tecniche di 
ricerca ibrida realizzata mediante Retrieval-Augmented Generation (RAG) e algoritmo di ranking BM25. 
L’architettura è pensata per garantire modularità, estendibilità e facilità di manutenzione, ed è stata 
realizzata applicando best practices come dependecy injection, e pattern specifici per la risoluzione di 
problemi ricorrenti riscontratu durante la realizzazione del software.

Il plugin implementa quattro funzionalità principali, ciascuna orchestrata da moduli dedicati, che coprono 
la generazione di comandi Git, la creazione di messaggi di commit, l’analisi dell’impatto delle modifiche 
e la risoluzione automatica dei conflitti.

#include "./module_1.typ"

#include "./module_2.typ"

#include "./module_3.typ"

#include "./module_4.typ"