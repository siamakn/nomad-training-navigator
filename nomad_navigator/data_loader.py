import pandas as pd
from nomad_navigator.models import Resource

def load_resources_from_csv(convert_lists=False):
    try:
        df = pd.read_csv("resources.csv")
    except Exception:
        return []

    if convert_lists:
        def safe_list(val):
            if pd.isna(val):
                return []
            try:
                return [v.strip() for v in str(val).strip("[]").replace("'", "").split(",") if v.strip()]
            except:
                return []

        for col in ["topics", "keywords"]:
            if col in df.columns:
                df[col] = df[col].apply(safe_list)

    return [
        Resource(
            id=row["id"],
            resource_type=row["resource_type"],
            resource_subtype=row["resource_subtype"],
            format=row["format"],
            title=row["title"],
            url=row["url"],
            topics=row["topics"],
            keywords=row["keywords"],
            status_tag=row["status_tag"],
            difficulty=row["difficulty"]
        )
        for _, row in df.iterrows()
    ]

def save_resources_to_csv(resources, convert_lists=False):
    df = pd.DataFrame([r.__dict__ for r in resources])

    # Ensure proper structure even when DataFrame is empty
    if df.empty:
        df = pd.DataFrame(columns=["id", "resource_type", "resource_subtype", "format", "title", "url", "topics", "keywords", "status_tag", "difficulty"])
    else:
        df["topics"] = df["topics"].apply(lambda lst: ", ".join(lst) if isinstance(lst, list) else lst)
        df["keywords"] = df["keywords"].apply(lambda lst: ", ".join(lst) if isinstance(lst, list) else lst)
        df = df[["id", "resource_type", "resource_subtype", "format", "title", "url", "topics", "keywords", "status_tag", "difficulty"]]

    df.to_csv("resources.csv", index=False)