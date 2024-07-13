import json
import os
from typing import List, Dict, Any

from src.core.contributions import get_final_contributors_list

def get_contributors() -> List[Dict[str, Any]]:
    contributions_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        ".contributions.json",
    )
    try:
        with open(contributions_file, "r") as f:
            contributions_data = json.load(f)
    except FileNotFoundError:
        print(f"Contributions file not found: {contributions_file}")
        return []

    contributors = get_final_contributors_list(contributions_data)

    for contributor in contributors:
        contributor["last_used_timestamp"] = max(
            contributions_data["identities"][email]["last_used_timestamp"]
            for email in contributor["emails"]
        )

    contributors.sort(key=lambda x: x["last_used_timestamp"], reverse=True)

    return contributors
