import pdfplumber


class PDFExtractAdapter:
    def __init__(self):
        pass

    def extract_text(self, file_path):
        # pdf_file_path = "data/rag_docs/gost_56939_2024.pdf"

        pages_text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                pages_text.append(t)

        full_text = "\n\n".join(pages_text)
        return full_text
