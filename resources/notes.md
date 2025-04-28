# Possibili LLM oer la generazione di codice:

## Code LLaMA (7B) - Quantizzato
**Pro:** Modello open-source di Meta ottimizzato per codice, ottima qualità.

**Come usarlo:** Usa una versione quantizzata a 4-bit (GGUF) tramite llama.cpp o ollama.

**Requisiti:** Una GTX 1650 riesce a gestire versioni quantizzate di modelli da 7B con un po’ di swap su RAM.

**RAG:** Si può integrare facilmente in pipeline RAG (es. con LangChain o LlamaIndex).


## StarCoder (o StarCoder2 3B)
**Pro:** Ottimo per codice, supporta molti linguaggi, versione da 3B adatta a GPU modeste.

**Come usarlo:** Versione 3B o 7B quantizzata. Supportato in Transformers o quantizzato in GGUF.

**RAG:** Ottimo abbinato a RAG, anche perché molto "data-aware".


## Phi-2 (di Microsoft)
**Pro:** Super leggero (2.7B), ottima qualità per quanto è piccolo.

**Contro:** Non è specializzato solo in codice, ma ha buone performance generali.

**RAG:** Integrabile facilmente con strumenti standard.

