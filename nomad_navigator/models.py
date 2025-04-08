from dataclasses import dataclass
from typing import List

@dataclass
class Resource:
    title: str
    url: str
    resource_type: str  # e.g. "Video", "Page", "Misc"
    topics: List[str]
    keywords: List[str]
    status_tag: str
    difficulty: str