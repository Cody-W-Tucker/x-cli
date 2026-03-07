"""
Recent Post Counts - X API v2
=============================
Endpoint: GET https://api.x.com/2/tweets/counts/recent
Docs: https://developer.x.com/en/docs/twitter-api/tweets/counts/api-reference/get-tweets-counts-recent

Authentication: Bearer Token (App-only)
Required env vars: BEARER_TOKEN

Note: Returns count of posts from the last 7 days matching your query.
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

query = "from:XDevelopers"

def main():
    # Get counts with automatic pagination
    all_counts = []
    for page in client.posts.get_counts_recent(
        query=query,
        granularity="day"
    ):
        # Access data attribute (model uses extra='allow' so data should be available)
        # Use getattr with fallback in case data field is missing from response
        page_data = getattr(page, 'data', []) or []
        all_counts.extend(page_data)
        print(f"Fetched {len(page_data)} count buckets (total: {len(all_counts)})")
    
    print(f"\nTotal Count Buckets: {len(all_counts)}")
    print(json.dumps({"data": all_counts}, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
