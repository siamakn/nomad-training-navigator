import pandas as pd
from typing import List
from nomad_navigator.models import Resource

CSV_FILE = "resources.csv"

def load_resources_from_csv(csv_path: str = CSV_FILE) -> List[Resource]:
    df = pd.read_csv(csv_path)
    return [
        Resource(
            title=row["title"],
            url=row["url"],
            resource_type=row["resource_type"],
            topics=row["topics"].split(";"),
            keywords=row["keywords"].split(";"),
            status_tag=row["status_tag"],
            difficulty=row["difficulty"]
        ) for _, row in df.iterrows()
    ]

def save_resources_to_csv(resources: List[Resource], csv_path: str = CSV_FILE):
    data = [
        {
            "title": r.title,
            "url": r.url,
            "resource_type": r.resource_type,
            "topics": ";".join(r.topics),
            "keywords": ";".join(r.keywords),
            "status_tag": r.status_tag,
            "difficulty": r.difficulty
        } for r in resources
    ]
    pd.DataFrame(data).to_csv(csv_path, index=False)