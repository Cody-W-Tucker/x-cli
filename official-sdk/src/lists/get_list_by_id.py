"""
List Lookup by ID - X API v2
=============================
Endpoint: GET https://api.x.com/2/lists/:id
Docs: https://developer.x.com/en/docs/twitter-api/lists/list-lookup/api-reference/get-lists-id

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
if not bearer_token:
    raise ValueError("BEARER_TOKEN environment variable is not set")

client = Client(bearer_token=bearer_token)

# You can replace the ID given with the List ID you wish to lookup.
list_id = "list-id"

def main():
    # List fields are adjustable. Options include:
    # created_at, follower_count, member_count, private, description, owner_id
    response = client.lists.get_by_id(
        list_id,
        list_fields=["created_at", "follower_count", "member_count", "owner_id", "description"]
    )
    
    print(json.dumps(response.data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
