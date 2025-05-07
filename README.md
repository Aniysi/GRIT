# GRIT

## Introduzione

GRIT è un plugin per Git scritto in Python. Il plugin utilizza la versatilità degli LLM per generare comandi Git a partire da indicazioni fornite in linguaggio naturale dall'utente. GRIT può anche essere usato per la crezione di commenti di commit templetizzati a partire dalle modifiche effettivamente apportate alla codebase, e dalle indicazioni dell'utente.

## Istruzioni per l'uso

### Requisiti tecnologici

Di seguito sono indicati i requsiti necessari per l'esecuzione del plugin, suddivisi in requsiti essenziali e non.

#### Requsiti essenziali

Per il funzionamento del software sono necessari nella macchina ospite:

- **Ollama** (versione 0.6.6 o superiore), con modello di embedding *mxbai-embed-large*, e un modello LLM general purpose a propria discrezione (nel progetto sono stati usati Qwen3 quantizzato con 4B parametri, e Gemma quantizzato con 3B di parametri);
- **Python** (versione 3.13.0 o superiore);
- Sistema operativo **Windows** (versione 10 o superiore).

#### Requisiti non essenziali

Di seguito sono indicati ulteriori requisiti utili solo a chi volesse ampliare il contenuto informativo su cui è stata effettuata l'operazione di RAG (Retrival Augmented Generation):

- **wkhtmltopdf** (versione 0.12.6 o superiore);
- libreria Python **pdfkit**

Di base il plugin implementa una pipeline RAG che contiene già l'intera documetazione di Git (recuperata dalla repository <https://github.com/git/htmldocs>). Se si vogliono aggiungere ulteriori contenuti (in formato *.html*), è necessario disporre tali file all'interno della directory *docs/htmldocs*, ed effettuare la loro conversione in pdf mediante il comando:

```bash
python docs/convertToPdf.py
```

In un momento successivo andrà quindi effettuato l'embedding dei file convertiti, mediante l'esecuzione del comando:

```bash
python src/embedding/__init__.py
```

attraverso l'ambiente virtuale Python accessibile con il comando:

```bash
src/venv/Scripts/activate
```

