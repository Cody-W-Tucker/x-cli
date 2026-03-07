"""
Full-Archive Search - X API v2
==============================
Endpoint: GET https://api.x.com/2/tweets/search/all
Docs: https://developer.x.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all

Authentication: Bearer Token (App-only)
Required env vars: BEARER_TOKEN

Note: Requires Academic Research access. Returns posts from the entire archive.
This example demonstrates automatic pagination using the iterate() method
to fetch all pages of results.
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

query = '(from:xdevelopers -is:retweet) OR #xdevelopers'

def main():
    # Search with automatic pagination
    all_posts = []
    for page in client.posts.search_all(
        query=query,
        max_results=100,  # Per page
        tweet_fields=["author_id", "created_at"]
    ):
        # Access data attribute (model uses extra='allow' so data should be available)
        # Use getattr with fallback in case data field is missing from response
        page_data = getattr(page, 'data', []) or []
        all_posts.extend(page_data)
        print(f"Fetched {len(page_data)} Posts (total: {len(all_posts)})")
    
    print(f"\nTotal Posts: {len(all_posts)}")
    print(json.dumps({"data": all_posts[:5]}, indent=4, sort_keys=True))  # Print first 5 as example


if __name__ == "__main__":
    main()