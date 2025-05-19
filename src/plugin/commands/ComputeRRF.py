from plugin.commands.BaseCommand import Command

from typing import List

class ComputeRRF(Command):
    def __init__(self, docs: List, n_res: int =10, k: int =60):
        self._documents = docs
        self._n_results = n_res
        self._k = k

    def getStructuredResults(self, rrf_scores):
        # Create sorted indices based on rrf_scores in descending order
        sorted_indices = sorted(range(len(rrf_scores)), key=lambda k: rrf_scores[k], reverse=True)[:self._n_results]
        
        results = {
            "command": [[self._documents['metadatas'][0][i]['full_command'] for i in sorted_indices]],
            "description": [[self._documents['documents'][0][i] for i in sorted_indices]],
            "rrf_scores": [rrf_scores[i] for i in sorted_indices]
        }
        return results

    def execute(self):
        import numpy as np
        dense_scores = np.array(self._documents['distances'][0])
        sparse_scores = np.array(self._documents['sparse_distances'])

        # Convert dense scores (where lower is better) to ranks
        dense_ranks = (-dense_scores).argsort().argsort() + 1
        
        # Convert sparse scores (where higher is better) to ranks
        sparse_ranks = (-sparse_scores).argsort().argsort() + 1

        # Calculate RRF scores
        rrf_scores = []
        for dense_rank, sparse_rank in zip(dense_ranks, sparse_ranks):
            # RRF formula: 1/(k + r) where k is a constant and r is the rank
            dense_rrf = 1 / (self._k + dense_rank)
            sparse_rrf = 1 / (self._k + sparse_rank)
            # Combine the RRF scores
            combined_rrf = dense_rrf + sparse_rrf
            rrf_scores.append(combined_rrf)

        return self.getStructuredResults(rrf_scores)