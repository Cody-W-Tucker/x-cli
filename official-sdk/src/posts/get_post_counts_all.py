"""
Full-Archive Post Counts - X API v2
===================================
Endpoint: GET https://api.x.com/2/tweets/counts/all
Docs: https://developer.x.com/en/docs/twitter-api/tweets/counts/api-reference/get-tweets-counts-all

Authentication: Bearer Token (App-only)
Required env vars: BEARER_TOKEN

Note: Requires Academic Research access. Returns counts from the entire archive.
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

query = "from:XDevelopers"

def main():
    # Get counts with automatic pagination
    # Optional: You can add start_time parameter to limit the date range
    # Example: start_time="2021-01-01T00:00:00Z"
    all_counts = []
    for page in client.posts.get_counts_all(
        query=query,
        granularity="day"
        # start_time="2021-01-01T00:00:00Z"  # Optional: uncomment to add date range
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
