import io

import pandas as pd

from app.services.file_parsers.base_parser import BaseFileParser


class ExcelParser(BaseFileParser):
    async def parse(self, file_content: bytes) -> pd.DataFrame:
        return pd.read_excel(io.BytesIO(file_content), engine="openpyxl")
