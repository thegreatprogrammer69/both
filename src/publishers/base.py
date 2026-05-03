from abc import ABC, abstractmethod


class Publisher(ABC):
    @abstractmethod
    async def publish(self, text: str, media_path: str | None = None) -> str:
        """Returns external publication id"""
