"""
Bookmarks Lookup - X API v2
===========================
Endpoint: GET https://api.x.com/2/users/:id/bookmarks
Docs: https://developer.x.com/en/docs/twitter-api/bookmarks/api-reference/get-users-id-bookmarks

Authentication: OAuth 2.0 (User Context)
Required env vars: CLIENT_ID, CLIENT_SECRET
"""

import os
import json
from xdk import Client
from xdk.oauth2_auth import OAuth2PKCEAuth

# The code below sets the client ID and client secret from your environment variables
# To set environment variables on macOS or Linux, run the export commands below from the terminal:
# export CLIENT_ID='YOUR-CLIENT-ID'
# export CLIENT_SECRET='YOUR-CLIENT-SECRET'
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
redirect_uri = "https://example.com"

# Set the scopes
scopes = ["bookmark.read", "tweet.read", "users.read", "offline.access"]

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
    
    # Step 6: Get authenticated user ID
    user_me = client.users.get_me()
    user_id = user_me.data["id"]
    
    # Step 7: Get bookmarks with automatic pagination
    all_bookmarks = []
    for page in client.users.get_bookmarks(
        user_id,
        max_results=100,
        tweetfields=["created_at"]
    ):
        all_bookmarks.extend(page.data)
        print(f"Fetched {len(page.data)} bookmarks (total: {len(all_bookmarks)})")
    
    print(f"\nTotal Bookmarks: {len(all_bookmarks)}")
    print(json.dumps({"data": all_bookmarks[:5]}, indent=4, sort_keys=True))  # Print first 5 as example

if __name__ == "__main__":
    main()
