"""
User Lookup - X API v2
======================
Endpoint: GET https://api.x.com/2/users/by
Docs: https://developer.x.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# Specify the usernames that you want to lookup (list, up to 100)
usernames = ["XDevelopers", "API"]

def main():
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    response = client.users.get_by_usernames(
        usernames=usernames,
        user_fields=["description", "created_at"]
    )
    
    # Access data attribute safely
    response_data = getattr(response, 'data', None)
    if response_data:
        print(json.dumps(response_data, indent=4, sort_keys=True))
    else:
        print(json.dumps(response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
