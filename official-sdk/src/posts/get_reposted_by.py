"""
Retweeted By (Users who reposted) - X API v2
============================================
Endpoint: GET https://api.x.com/2/tweets/:id/retweeted_by
Docs: https://developer.x.com/en/docs/twitter-api/tweets/retweets/api-reference/get-tweets-id-retweeted_by

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# You can replace the ID given with the Post ID you wish to lookup reposting users for
# You can find an ID by using the Post lookup endpoint
post_id = "post-id"

def main():
    # Get reposted by users with automatic pagination
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    all_users = []
    for page in client.posts.get_reposted_by(
        post_id,
        max_results=100,
        user_fields=["created_at", "description"]
    ):
        # Access data attribute (model uses extra='allow' so data should be available)
        # Use getattr with fallback in case data field is missing from response
        page_data = getattr(page, 'data', []) or []
        all_users.extend(page_data)
        print(f"Fetched {len(page_data)} users (total: {len(all_users)})")
    
    print(f"\nTotal Users: {len(all_users)}")
    print(json.dumps({"data": all_users[:5]}, indent=4, sort_keys=True))  # Print first 5 as example

if __name__ == "__main__":
    main()
