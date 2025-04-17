def generate_sequential_id(resources):
    existing_ids = [
        int(r.id) for r in resources
        if isinstance(r.id, str) and r.id.isdigit() and len(r.id) == 4
    ]
    next_id = max(existing_ids, default=0) + 1
    return f"{next_id:04d}"
