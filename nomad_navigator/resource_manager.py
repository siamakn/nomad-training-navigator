from typing import List, Optional
from nomad_navigator.models import Resource

def filter_resources(
    resources: List[Resource],
    topic: Optional[str] = None,
    keyword: Optional[str] = None,
    tag: Optional[str] = None,
    difficulty: Optional[str] = None
) -> List[Resource]:
    filtered = resources
    if topic:
        filtered = [r for r in filtered if topic in r.topics]
    if keyword:
        filtered = [r for r in filtered if keyword in r.keywords]
    if tag:
        filtered = [r for r in filtered if r.status_tag == tag]
    if difficulty:
        filtered = [r for r in filtered if r.difficulty == difficulty]
    return filtered