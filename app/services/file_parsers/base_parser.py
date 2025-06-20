from abc import ABC, abstractmethod
import pandas as pd


class BaseFileParser(ABC):
    @abstractmethod
    async def parse(self, file_content: bytes) -> pd.DataFrame:
        pass
