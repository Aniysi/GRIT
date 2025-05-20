from plugin.commands.GetSparseEmbeddings import GetSparseEmbeddings

import pytest
from unittest.mock import patch, MagicMock
from rank_bm25 import BM25Okapi
from typing import Dict

class TestGetSparseEmbeddings:
    def setup_method(self):
        # Sample docs for testing
        self.docs = {
            'ids': [['git commit_0', 'git branch_0', 'git log_0', 'git add_0', 'git checkout_0']],
            'embeddings': None,
            'documents': [[
                'Voglio salvare i cambiamenti che ho messo in staging creando un nuovo commit.',
                'Voglio vedere la lista di tutti i branch locali disponibili nel mio repository.',
                'Voglio vedere solo autore e messaggio per ogni commit, in una sola riga.',
                "Voglio aggiungere tutti i file modificati all'area di staging, ma non voglio includere quelli nuovi non tracciati.",
                'Voglio passare a un branch che esiste già per continuare a lavorare lì.'
            ]],
            'metadatas': [[{
                'keywords': 'salvare modifiche nuovo commit staging git commit',
                'full_command': 'git commit',
                'command': 'git commit'
            }, {
                'full_command': 'git branch',
                'command': 'git branch',
                'keywords': 'vedere lista branch locali git branch'
            }, {
                'full_command': 'git log --pretty=oneline',
                'keywords': 'log autore messaggio lista commit oneline storico',
                'command': 'git log'
            }, {
                'keywords': 'aggiungere tutti modificati escludere non tracciati staging',
                'command': 'git add',
                'full_command': 'git add .'
            }, {
                'command': 'git checkout',
                'full_command': 'git checkout nome-branch',
                'keywords': 'cambiare branch passare esistente checkout spostarsi'
            }]]
        }
        self.query = "Mostrami il log dei commit con grafo."
        self.get_sparse = GetSparseEmbeddings(self.docs, self.query)

    def test_tokenization(self):
        # Test if tokenization works correctly by checking the _tokenized_corpus attribut of GetSparseEmbeddings object
        tokens = self.get_sparse._tokenized_corpus[0]
        assert isinstance(tokens, list)
        assert all(isinstance(token, str) for token in tokens)
        assert "salvare" in tokens
        assert "commit" in tokens

    def test_empty_docs(self):
        # Test with empty docs
        empty_docs = {
            'ids': [[]],
            'documents': [[]],
            'metadatas': [[]]
        }
        with pytest.raises(ValueError):
            GetSparseEmbeddings(empty_docs, self.query)

    def test_empty_query(self):
        # Test with empty docs
        empty_query = ""
        with pytest.raises(ValueError):
            GetSparseEmbeddings(self.docs, empty_query)

    def test_none_docs(self):
        # Test with None docs
        with pytest.raises(TypeError):
            GetSparseEmbeddings(None, self.query)

    def test_none_query(self):
        # Test with None docs
        with pytest.raises(TypeError):
            GetSparseEmbeddings(self.docs, None)

    def test_execute_returns_scores(self):
        # Test if execute returns valid scores
        result = self.get_sparse.execute()
        
        assert isinstance(result, Dict)
        assert len(result['documents'][0]) == len(self.docs['documents'][0])
        assert all(isinstance(score, float) for score in result['sparse_distances'])

    def test_single_document(self):
        # Test with single document
        single_docs = {
            'ids': [['git commit_0']],
            'documents': [['Voglio salvare i cambiamenti che ho messo in staging creando un nuovo commit.']],
            'metadatas': [[{'keywords': 'salvare modifiche nuovo commit staging git commit'}]]
        }
        single_get_sparse = GetSparseEmbeddings(single_docs, self.query)
        result = single_get_sparse.execute()
        
        assert isinstance(result, Dict)
        assert len(result['documents']) == 1
        assert isinstance(result['sparse_distances'][0], float)