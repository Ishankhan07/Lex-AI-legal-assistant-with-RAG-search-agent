from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextChunker:

    def __init__(self, chunk_size=1200, chunk_overlap=100):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def create_chunks(self, text):

        return self.text_splitter.split_text(text)