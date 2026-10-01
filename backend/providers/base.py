from abc import ABC, abstractmethod

import pandas as pd


class DataProvider(ABC):
    @abstractmethod
    def fetch_prices(self, symbols: list[str], start: str, end: str | None = None) -> pd.DataFrame:
        ...

    @abstractmethod
    def fetch_actions(self, symbols: list[str]) -> pd.DataFrame:
        ...

    @abstractmethod
    def fetch_fundamentals(self, symbol: str) -> dict:
        ...
