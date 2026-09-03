from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProvider(ABC):
    """
    Standard interface for all data providers.
    Providers return normalized dictionaries that conform to the ContentItem schema.
    """

    def __init__(self, name: str, source_type: str):
        self.name = name
        self.source_type = source_type

    @abstractmethod
    async def fetch_items(self) -> List[Dict[str, Any]]:
        """Fetch and return list of normalized raw item dicts."""
        pass
