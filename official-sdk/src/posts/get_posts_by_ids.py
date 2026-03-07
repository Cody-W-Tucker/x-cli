"""
Post Lookup - X API v2
======================
Endpoint: GET https://api.x.com/2/tweets
Docs: https://developer.x.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets

Authentication: Bearer Token (App-only) or OAuth (User Context)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# Post IDs to look up (comma-separated list, up to 100)
# You can adjust ids to include a single Post or add up to 100 comma-separated IDs
post_ids = ["post-id-1", "post-id-2"]

def main():
    # Post fields are adjustable. Options include:
    # attachments, author_id, context_annotations, conversation_id,
    # created_at, entities, geo, id, in_reply_to_user_id, lang,
    # non_public_metrics, organic_metrics, possibly_sensitive,
    # promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    response = client.posts.get_by_ids(
        ids=post_ids,
        tweet_fields=["created_at", "author_id", "lang", "source", "public_metrics", "context_annotations", "entities"]
    )
    
    print(json.dumps(response.data, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
