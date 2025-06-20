import io

import pandas as pd

from app.services.file_parsers.base_parser import BaseFileParser


class TXTParser(BaseFileParser):
    async def parse(self, file_content: bytes) -> pd.DataFrame:
        content_str = file_content.decode("utf-8")
        return pd.read_csv(io.StringIO(content_str), sep=r"\s+")
