from pathlib import Path
class Documents:
    def read_pdf_page(self,path,page=1):
        import fitz
        doc=fitz.open(path); return doc[page-1].get_text()
    def read_docx(self,path):
        from docx import Document
        return "\\n".join(p.text for p in Document(path).paragraphs)
    def read_text(self,path): return Path(path).read_text(encoding="utf-8",errors="replace")
