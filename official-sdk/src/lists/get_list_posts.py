"""
List Tweets - X API v2
======================
Endpoint: GET https://api.x.com/2/lists/:id/tweets
Docs: https://developer.x.com/en/docs/twitter-api/lists/list-tweets/api-reference/get-lists-id-tweets

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# Be sure to replace list-id with any List ID
list_id = "list-id"

def main():
    # Get list tweets with automatic pagination
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    all_posts = []
    for page in client.lists.get_posts(
        list_id,
        max_results=100,
        tweet_fields=["lang", "author_id"]
    ):
        # Access data attribute (model uses extra='allow' so data should be available)
        # Use getattr with fallback in case data field is missing from response
        page_data = getattr(page, 'data', []) or []
        all_posts.extend(page_data)
        print(f"Fetched {len(page_data)} posts (total: {len(all_posts)})")
    
    print(f"\nTotal Posts: {len(all_posts)}")
    print(json.dumps({"data": all_posts[:5]}, indent=4, sort_keys=True))  # Print first 5 as example

if __name__ == "__main__":
    main()
