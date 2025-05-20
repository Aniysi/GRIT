from plugin.commands.BaseCommand import Command

from rank_bm25 import BM25Okapi
from typing import Dict

class GetSparseEmbeddings(Command):
    def __init__(self, docs: Dict, query: str):
        if not isinstance(docs, Dict):
            raise TypeError(f"Param docs must be a Dict, not {type(docs)}")
        if not docs or not docs.get('metadatas') or not docs['metadatas'][0]:
            raise ValueError("Documents list or metadata is empty")
        self._documents_list = docs
        self._tokenized_corpus = [doc['keywords'].split() for doc in self._documents_list['metadatas'][0]]
        self._bm25 = BM25Okapi(self._tokenized_corpus)
        if not isinstance(query, str):
            raise TypeError(f"Param query must be a string, not {type(query)}")
        if not query.strip():
            raise ValueError("Query string cannot be empty")
        self._tokenized_query = query.split()

    def execute(self):
        sparse_scores = self._bm25.get_scores(self._tokenized_query)
        self._documents_list['sparse_distances'] = list(sparse_scores)
        return self._documents_list