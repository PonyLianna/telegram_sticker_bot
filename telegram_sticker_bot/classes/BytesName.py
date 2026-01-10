from dataclasses import dataclass


@dataclass
class BytesName:
    name: str
    content: bytes
