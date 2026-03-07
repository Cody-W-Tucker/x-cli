"""
User Followers Lookup - X API v2
================================
Endpoint: GET https://api.x.com/2/users/:id/followers
Docs: https://developer.x.com/en/docs/twitter-api/users/follows/api-reference/get-users-id-followers

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# Replace with the user ID you want to get followers for
user_id = "2244994945"

def main():
    # Get followers with automatic pagination
    all_users = []
    for page in client.users.get_followers(
        user_id,
        max_results=100,
        user_fields=["created_at"]
    ):
        # Access data attribute (model uses extra='allow' so data should be available)
        # Use getattr with fallback in case data field is missing from response
        page_data = getattr(page, 'data', []) or []
        all_users.extend(page_data)
        print(f"Fetched {len(page_data)} users (total: {len(all_users)})")
    
    print(f"\nTotal Followers: {len(all_users)}")
    print(json.dumps({"data": all_users[:5]}, indent=4, sort_keys=True))  # Print first 5 as example

if __name__ == "__main__":
    main()
