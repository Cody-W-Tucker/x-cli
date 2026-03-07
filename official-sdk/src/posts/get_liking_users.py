"""
Liking Users - X API v2
======================
Endpoint: GET https://api.x.com/2/tweets/:id/liking_users
Docs: https://developer.x.com/en/docs/twitter-api/tweets/likes/api-reference/get-tweets-id-liking_users

Authentication: OAuth 2.0 (User Context)
Required env vars: CLIENT_ID, CLIENT_SECRET
"""

import os
import json
from xdk import Client
from xdk.oauth2_auth import OAuth2PKCEAuth
from requests.exceptions import HTTPError

# The code below sets the client ID and client secret from your environment variables
# To set environment variables on macOS or Linux, run the export commands below from the terminal:
# export CLIENT_ID='YOUR-CLIENT-ID'
# export CLIENT_SECRET='YOUR-CLIENT-SECRET'
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
redirect_uri = "https://example.com"

# Set the scopes
scopes = ["tweet.read", "users.read", "like.read", "offline.access"]

# You can replace the ID given with the Post ID you wish to get liking users for.
# You can find an ID by using the Post lookup endpoint
post_id = "post-id"

def main():
    # Step 1: Create PKCE instance
    auth = OAuth2PKCEAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes
    )
    
    # Step 2: Get authorization URL
    auth_url = auth.get_authorization_url()
    print("Visit the following URL to authorize your App on behalf of your X handle in a browser:")
    print(auth_url)
    
    # Step 3: Handle callback
    callback_url = input("Paste the full callback URL here: ")
    
    # Step 4: Exchange code for tokens
    tokens = auth.fetch_token(authorization_response=callback_url)
    access_token = tokens["access_token"]
    
    # Step 5: Create client
    client = Client(access_token=access_token)
    
    # Step 6: Get liking users with automatic pagination
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    all_users = []
    for page in client.posts.get_liking_users(
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
