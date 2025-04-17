from dataclasses import dataclass
from typing import List

@dataclass
class Resource:
    id: str
    resource_type: str
    resource_subtype: str
    format: str
    title: str
    url: str
    topics: List[str]
    keywords: List[str]
    status_tag: str
    difficulty: str