"""
Quote Tweets Lookup - X API v2
==============================
Endpoint: GET https://api.x.com/2/tweets/:id/quote_tweets
Docs: https://developer.x.com/en/docs/twitter-api/tweets/quote-tweets/api-reference/get-tweets-id-quote_tweets

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# Replace with the post ID you want to get quotes for
post_id = "1409931481552543749"

def main():
    # Get quote tweets with automatic pagination
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    all_posts = []
    for page in client.posts.get_quoted(
        post_id,
        max_results=100,
        tweet_fields=["created_at"]
    ):
        all_posts.extend(page.data)
        print(f"Fetched {len(page.data)} posts (total: {len(all_posts)})")
    
    print(f"\nTotal Quote Tweets: {len(all_posts)}")
    print(json.dumps({"data": all_posts[:5]}, indent=4, sort_keys=True))  # Print first 5 as example

if __name__ == "__main__":
    main()
    