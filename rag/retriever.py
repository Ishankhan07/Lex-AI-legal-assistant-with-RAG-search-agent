import os
import faiss
import pickle
import numpy as np

from models.embedding import EmbeddingModel


class Retriever:

    def __init__(
        self,
        index_path="vector_db/index.faiss",
        chunk_path="vector_db/chunks.pkl"
    ):

        self.index_path = index_path
        self.chunk_path = chunk_path


        # Check FAISS index exists

        if not os.path.exists(self.index_path):

            raise FileNotFoundError(
                f"FAISS Index not found : {self.index_path}"
            )


        if not os.path.exists(self.chunk_path):

            raise FileNotFoundError(
                f"Chunk file not found : {self.chunk_path}"
            )


        # Load FAISS

        self.index = faiss.read_index(
            self.index_path
        )


        # Load chunks

        with open(
            self.chunk_path,
            "rb"
        ) as f:

            self.chunks = pickle.load(f)



        # Load embedding model

        self.embedding_model = EmbeddingModel()



        print(
            f"Retriever Loaded ✅ ({self.index.ntotal} vectors)"
        )



    def search(
        self,
        query,
        top_k=3
    ):


        # Convert query into embedding

        query_embedding = self.embedding_model.get_embeddings(
            [query]
        )


        query_embedding = np.array(
            query_embedding
        ).astype("float32")



        # FAISS search

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )



        results = []


        for idx, score in zip(
            indices[0],
            scores[0]
        ):


            if idx == -1:
                continue


            results.append(
                {
                    "text": self.chunks[idx],
                    "score": float(score)
                }
            )



        return results



if __name__ == "__main__":


    retriever = Retriever()


    question = (
        "What is Bharatiya Nagarik "
        "Suraksha Sanhita 2023?"
    )


    results = retriever.search(
        question,
        top_k=3
    )


    for i, result in enumerate(results):

        print("\n================")
        print("Result:", i+1)
        print("Score:", result["score"])
        print(result["text"][:500])