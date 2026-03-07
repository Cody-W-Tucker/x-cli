"""
Sampled Stream (1% Volume) - X API v2
=====================================
Endpoint: GET https://api.x.com/2/tweets/sample/stream
Docs: https://developer.x.com/en/docs/twitter-api/tweets/volume-streams/api-reference/get-tweets-sample-stream

Authentication: Bearer Token (App-only)
Required env vars: BEARER_TOKEN

Note: Returns approximately 1% of all public posts in real-time.
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

def main():
    # Stream posts in real-time
    for post in client.stream.posts_sample():
        print(json.dumps(post.data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
