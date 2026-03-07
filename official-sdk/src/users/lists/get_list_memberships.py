"""
User List Memberships Lookup - X API v2
=======================================
Endpoint: GET https://api.x.com/2/users/:id/list_memberships
Docs: https://developer.x.com/en/docs/twitter-api/lists/list-members/api-reference/get-users-id-list_memberships

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# You can replace the user-id with any valid User ID you wish to find what Lists they are members of.
user_id = "user-id"

def main():
    # Get user list memberships with automatic pagination
    # List fields are adjustable, options include:
    # created_at, description, owner_id,
    # private, follower_count, member_count,
    all_lists = []
    for page in client.users.get_list_memberships(
        user_id,
        max_results=100,
        list_fields=["created_at", "follower_count"]
    ):
        # Access data attribute (model uses extra='allow' so data should be available)
        # Use getattr with fallback in case data field is missing from response
        page_data = getattr(page, 'data', []) or []
        all_lists.extend(page_data)
        print(f"Fetched {len(page_data)} lists (total: {len(all_lists)})")
    
    print(f"\nTotal List Memberships: {len(all_lists)}")
    print(json.dumps({"data": all_lists[:5]}, indent=4, sort_keys=True))  # Print first 5 as example

if __name__ == "__main__":
    main()
