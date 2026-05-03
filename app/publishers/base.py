from abc import ABC, abstractmethod


class Publisher(ABC):
    @abstractmethod
    async def publish(self, text: str, image_path: str | None = None, video_path: str | None = None) -> str:
        raise NotImplementedError
