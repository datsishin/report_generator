import pandas as pd

from fastapi import UploadFile

from app.services.file_parsers.excel_parser import ExcelParser
from app.services.file_parsers.tsv_parser import TSVParser
from app.services.file_parsers.txt_parser import TXTParser


class FileService:
    _parsers = {
        '.xlsx': ExcelParser(),
        '.tsv': TSVParser(),
        '.txt': TXTParser(),
    }

    @staticmethod
    async def parse_file(file: UploadFile) -> pd.DataFrame:
        file_extension = file.filename.split('.')[-1].lower()
        parser = FileService._parsers.get(f'.{file_extension}')

        if not parser:
            raise ValueError(f"Unsupported file format: {file_extension}")

        file_content = await file.read()
        return await parser.parse(file_content)
