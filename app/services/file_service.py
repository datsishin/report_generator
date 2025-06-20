from typing import ClassVar

import pandas as pd
from fastapi import UploadFile

from app.services.file_parsers.excel_parser import ExcelParser
from app.services.file_parsers.tsv_parser import TSVParser
from app.services.file_parsers.txt_parser import TXTParser


class FileService:
    _parsers: ClassVar[dict] = {
        ".xlsx": ExcelParser(),
        ".tsv": TSVParser(),
        ".txt": TXTParser(),
    }

    @staticmethod
    async def parse_file(file: UploadFile) -> pd.DataFrame:
        file_extension = file.filename.split(".")[-1].lower()
        parser = FileService._parsers.get(f".{file_extension}")

        if not parser:
            error_msg = f"Unsupported file format: {file_extension}"
            raise ValueError(error_msg)

        file_content = await file.read()
        return await parser.parse(file_content)
