import os
import pickle
import faiss
import numpy as np

from utils.pdf_loader import PDFLoader
from utils.chunking import TextChunker
from models.embedding import EmbeddingModel



class VectorStore:


    def __init__(
        self,
        pdf_folder="data/legal_docs",
        index_name="index.faiss",
        chunk_name="chunks.pkl"
    ):


        self.pdf_folder = pdf_folder

        self.save_path = "vector_db"


        self.index_path = os.path.join(
            self.save_path,
            index_name
        )


        self.chunk_path = os.path.join(
            self.save_path,
            chunk_name
        )


        self.loader = PDFLoader(
            self.pdf_folder
        )


        self.chunker = TextChunker()


        self.embedding_model = EmbeddingModel()



    def build_vector_store(self):


        pdf_files = self.loader.get_pdf_files()


        if len(pdf_files) == 0:


            print(
                "❌ No PDF files found."
            )

            return



        all_chunks = []



        print(
            "\nReading PDFs...\n"
        )



        for pdf in pdf_files:


            print(
                "Reading:",
                os.path.basename(pdf)
            )


            text = self.loader.extract_text(
                pdf
            )


            chunks = self.chunker.create_chunks(
                text
            )


            print(
                "Chunks:",
                len(chunks)
            )


            all_chunks.extend(
                chunks
            )



        print(
            "\nTotal chunks:",
            len(all_chunks)
        )



        print(
            "\nGenerating embeddings..."
        )



        embeddings = self.embedding_model.get_embeddings(
            all_chunks,
            batch_size=32
        )



        embeddings = np.array(
            embeddings
        ).astype("float32")



        dimension = embeddings.shape[1]



        print(
            "\nCreating FAISS index..."
        )



        index = faiss.IndexFlatIP(
            dimension
        )


        index.add(
            embeddings
        )



        print(
            "Vectors stored:",
            index.ntotal
        )



        os.makedirs(
            self.save_path,
            exist_ok=True
        )



        # Save FAISS

        faiss.write_index(
            index,
            self.index_path
        )



        # Save chunks

        with open(
            self.chunk_path,
            "wb"
        ) as f:


            pickle.dump(
                all_chunks,
                f
            )



        print(
            "\n✅ FAISS Database Created Successfully"
        )

        print(
            "Index:",
            self.index_path
        )

        print(
            "Chunks:",
            self.chunk_path
        )




if __name__ == "__main__":


    print(
        "Building Legal Knowledge Base..."
    )


    store = VectorStore()


    store.build_vector_store()