import os
import fitz  # PyMuPDF


class PDFLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_pdf_files(self):
        """Return all PDF files from the folder."""
        pdf_files = [
            os.path.join(self.folder_path, file)
            for file in os.listdir(self.folder_path)
            if file.lower().endswith(".pdf")
        ]
        return pdf_files

    def extract_text(self, pdf_path):
        """Extract text from a single PDF."""
        document = fitz.open(pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text


if __name__ == "__main__":

    pdf_folder = "data/legal_docs"

    loader = PDFLoader(pdf_folder)

    pdf_files = loader.get_pdf_files()

    print(f"\nFound {len(pdf_files)} PDF(s).\n")

    for pdf in pdf_files:
        print("=" * 60)
        print(f"Reading: {os.path.basename(pdf)}")

        extracted_text = loader.extract_text(pdf)

        print(f"Characters Extracted : {len(extracted_text)}")

        print("\nSample Text:\n")

        print(extracted_text[:700])

        print("\n")