import pytest
import numpy as np
from src.plugin.commands.ComputeRRF import ComputeRRF

class TestComputeRRF:
    def setup_method(self):
        # Test with empty docs
        self.empty_docs = {
            'ids': [[]],
            'documents': [[]],
            'metadatas': [[]],
            'distances': [[]],
            'sparse_distances': []
        }
        
        # Test with single document
        self.single_doc = {
            'ids': [['git commit_0']],
            'documents': [['Voglio salvare i cambiamenti che ho messo in staging creando un nuovo commit.']],
            'metadatas': [[{'full_command': 'git commit', 'keywords': 'salvare modifiche nuovo commit staging git commit', 'command': 'git commit'}]],
            'distances': [[0.6628900766372681]],
            'sparse_distances': [np.float64(0.4714897583227188)]
        }
        
        # Test with multiple documents
        self.multiple_docs = {
            'ids': [['git commit_0', 'git log_0', 'git branch_0']],
            'documents': [[
                'Voglio salvare i cambiamenti che ho messo in staging creando un nuovo commit.',
                'Voglio vedere solo autore e messaggio per ogni commit, in una sola riga.',
                'Voglio vedere la lista di tutti i branch locali disponibili nel mio repository.'
            ]],
            'metadatas': [[
                {'full_command': 'git commit', 'keywords': 'salvare modifiche nuovo commit staging git commit', 'command': 'git commit'},
                {'full_command': 'git log --pretty=oneline', 'keywords': 'log autore messaggio lista commit oneline storico', 'command': 'git log'},
                {'command': 'git branch', 'full_command': 'git branch', 'keywords': 'vedere lista branch locali git branch'}
            ]],
            'distances': [[0.6628900766372681, 0.7612106800079346, 0.8177884221076965]],
            'sparse_distances': [np.float64(0.4714897583227188), np.float64(0.3275393453834816), np.float64(0.0)]
        }

    def test_empty_docs(self):
        compute_rrf = ComputeRRF(self.empty_docs)
        result = compute_rrf.execute()
        assert len(result) == 3
        assert len(result['command'][0]) == 0

    def test_single_doc(self):
        compute_rrf = ComputeRRF(self.single_doc)
        result = compute_rrf.execute()
        assert len(result) == 3
        assert 'git commit' in result['command'][0]
        assert len(result['command']) == 1

    def test_multiple_docs(self):
        compute_rrf = ComputeRRF(self.multiple_docs)
        result = compute_rrf.execute()
        assert len(result['command'][0]) == 3
        assert all(doc in result['command'][0] for doc in ['git commit', 'git log --pretty=oneline', 'git branch'])
        # Documents with lower distances should have higher RRF scores
        assert result['rrf_scores'][0] >= result['rrf_scores'][1] >= result['rrf_scores'][2]

    def test_rrf_formula(self):
        compute_rrf = ComputeRRF(self.single_doc)
        result = compute_rrf.execute()
        k = 60  # Default k value for RRF
        expected = 1 / (k + 1)  # RRF formula for rank 1
        expected *= 2 # RRF scores are abotained throuth the sum of dense and sparse RRFs, so we multiply by 2
        assert abs(result['rrf_scores'][0] - expected) < 1e-6