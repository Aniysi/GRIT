from plugin.commands.BaseCommand import Command

from rank_bm25 import BM25Okapi
from typing import List

class GetSparseEmbeddings(Command):
    def __init__(self, docs: List, query: str):
        self._documents_list = docs
        self._tokenized_corpus = [doc['keywords'].split() for doc in self._documents_list['metadatas'][0]]
        self._bm25 = BM25Okapi(self._tokenized_corpus)
        self._tokenized_query = query.split()

    def execute(self):
        sparse_scores = self._bm25.get_scores(self._tokenized_query)
        self._documents_list['sparse_distances'] = list(sparse_scores)
        return self._documents_list