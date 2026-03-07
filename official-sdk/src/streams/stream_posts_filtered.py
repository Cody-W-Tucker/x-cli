"""
Filtered Stream - X API v2
==========================
Endpoint: GET https://api.x.com/2/tweets/search/stream
Docs: https://developer.x.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream

Authentication: Bearer Token (App-only)
Required env vars: BEARER_TOKEN

Note: Streams posts matching your filter rules in real-time.
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

def get_rules():
    response = client.stream.get_rules()
    # Access data attribute safely
    rules_data = getattr(response, 'data', None)
    if rules_data:
        print(json.dumps(rules_data, indent=4, sort_keys=True))
    return rules_data


def delete_all_rules(rules):
    if rules is None or not rules:
        return None

    ids = [rule["id"] for rule in rules]
    payload = {"delete": {"ids": ids}}
    response = client.stream.update_rules(body=payload)
    # Access data attribute safely
    response_data = getattr(response, 'data', None)
    if response_data:
        print(json.dumps(response_data, indent=4, sort_keys=True))


def set_rules():
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "dog has:images", "tag": "dog pictures"},
        {"value": "cat has:images -grumpy", "tag": "cat pictures"},
    ]
    payload = {"add": sample_rules}
    response = client.stream.update_rules(body=payload)
    # Access data attribute safely
    response_data = getattr(response, 'data', None)
    if response_data:
        print(json.dumps(response_data, indent=4, sort_keys=True))


def get_stream():
    # Stream posts matching the filter rules in real-time
    # The posts() method is the filtered stream
    try:
        for post in client.stream.posts():
            # Access data attribute safely
            post_data = getattr(post, 'data', None)
            if post_data:
                print(json.dumps(post_data, indent=4, sort_keys=True))
    except Exception as e:
        print(f"Error streaming posts: {e}")
        print("Note: This could be a temporary API issue (503 Service Unavailable)")
        print("or the stream endpoint may be experiencing issues.")
        raise


def main():
    rules = get_rules()
    delete_all_rules(rules)
    set_rules()
    get_stream()


if __name__ == "__main__":
    main()
