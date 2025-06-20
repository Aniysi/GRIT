from infrastructure.embedding.rag_pipeline_builder import AbstractRAGPipelineBuilder
from infrastructure.database.database_manager import DBManager

from rank_bm25 import BM25Okapi
import numpy as np

class RAGContextBuilder():
    def __init__(self, pipeline: AbstractRAGPipelineBuilder, database_manager: DBManager):
        self._pipeline = pipeline
        self._database_manager = database_manager
    
    def organize_retrived_docs(self, results):

        organized_docs = {
            'texts': [],
            'example_commands': [],
            'distances': []
        }
        
        for i in range(len(results['documents'][0])):
            organized_docs['texts'].append(results['documents'][0][i])
            organized_docs['example_commands'].append(results['metadatas'][0][i]['example_command'])
            organized_docs['distances'].append(results['distances'][0][i])
            
        return organized_docs

    def rank_docs_bm25(self, docs, query: str):

        # Create tokenized corpus
        tokenized_corpus = [text.split() for text in docs['texts']]
        bm25 = BM25Okapi(tokenized_corpus)
        # Create tokenized query
        tokenized_query = query.split()

        # Compute sparse scores
        scores = bm25.get_scores(tokenized_query)

        # Add scores to docs dictionary
        docs['scores'] = list(scores)
        return docs

    def compute_rrf_scores(self, docs, k: int = 60):
        dense_scores = np.array(docs['distances'])
        sparse_scores = np.array(docs['scores'])

        # Convert dense scores (where lower is better) to ranks
        dense_ranks = (-dense_scores).argsort().argsort() + 1
        # Convert sparse scores (where higher is better) to ranks
        sparse_ranks = (-sparse_scores).argsort().argsort() + 1

        # Calculate RRF scores
        rrf_scores = []
        for dense_rank, sparse_rank in zip(dense_ranks, sparse_ranks):
            # RRF formula: 1/(k + r) where k is a constant and r is the rank
            dense_rrf = 1 / (k + dense_rank)
            sparse_rrf = 1 / (k + sparse_rank)
            # Combine the RRF scores
            combined_rrf = dense_rrf + sparse_rrf
            rrf_scores.append(combined_rrf)
        docs['ranks'] = rrf_scores
    
        return docs
    
    def truncate_top_n(self, docs, n: int = 10):
        # Get indices of top n ranks
        top_indices = np.argsort(docs['ranks'])[-n:]
        # Sort indices in descending order by rank values
        top_indices = sorted(top_indices, key=lambda i: docs['ranks'][i], reverse=True)

        # Truncate each field to keep only top n elements in descending rank order
        docs['texts'] = [docs['texts'][i] for i in top_indices]
        docs['example_commands'] = [docs['example_commands'][i] for i in top_indices]
        docs['distances'] = [docs['distances'][i] for i in top_indices]
        docs['scores'] = [docs['scores'][i] for i in top_indices]
        docs['ranks'] = [docs['ranks'][i] for i in top_indices]

        return docs

    def build_context(self, query: str, model: str):

        # Get embedded query
        _, embeddings = self._pipeline.handle(query)

        # Retrive relevant documents
        docs = self.organize_retrived_docs(self._database_manager.query(embeddings, 20))

        # Rank docs with bm25
        docs = self.rank_docs_bm25(docs, query)

        # Compute rrf scores
        docs = self.compute_rrf_scores(docs)

        # Get top n docs
        docs = self.truncate_top_n(docs, 10)

        # Return formatted context
        formatted_context = ""
        for text, command in zip(docs['texts'], docs['example_commands']):
            formatted_context += f" - Description: {text}\n - Command: {command}\n\n"
        return formatted_context


        

