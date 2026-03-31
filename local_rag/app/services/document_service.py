import os
import uuid
from app.parsers.pdf_parser import PdfParser
from app.parsers.txt_parser import TxtParser
from app.parsers.markdown_parser import MarkdownParser
from app.core.logging import logger

class DocumentService:
    def __init__(self):
        self.parsers = {
            ".pdf": PdfParser(),
            ".txt": TxtParser(),
            ".md": MarkdownParser()
        }
        
    def save_raw_file(self, filename: str, content: bytes, save_dir: str) -> str:
        os.makedirs(save_dir, exist_ok=True)
        unique_id = str(uuid.uuid4())
        safe_filename = f"{unique_id}_{filename}"
        file_path = os.path.join(save_dir, safe_filename)
        
        with open(file_path, "wb") as f:
            f.write(content)
            
        return file_path

    def parse_document(self, file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        parser = self.parsers.get(ext)
        if not parser:
            logger.warning(f"No specific parser for {ext}, falling back to TXT.")
            parser = self.parsers[".txt"]
            
        return parser.parse(file_path)
