"""
Pinned Lists Lookup - X API v2
==============================
Endpoint: GET https://api.x.com/2/users/:id/pinned_lists
Docs: https://developer.x.com/en/docs/twitter-api/lists/pinned-lists/api-reference/get-users-id-pinned_lists

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
scopes = ["tweet.read", "users.read", "list.read", "offline.access"]

# Be sure to replace your-user-id with your own user ID or one of an authenticated user
# You can find a user ID by using the user lookup endpoint
user_id = "your-user-id"

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
    
    # Step 6: Get pinned lists
    # List fields are adjustable, options include:
    # created_at, description, owner_id,
    # private, follower_count, member_count,
    response = client.users.get_pinned_lists(
        user_id,
        list_fields=["created_at", "description", "private"]
    )
    
    # Access data attribute (model uses extra='allow' so data should be available)
    response_data = getattr(response, 'data', None)
    if response_data is None:
        # Try accessing via model_dump if data attribute doesn't exist
        response_dict = response.model_dump() if hasattr(response, 'model_dump') else {}
        response_data = response_dict.get('data', response_dict)
    
    print(f"Total Pinned Lists: {len(response_data) if isinstance(response_data, list) else 1}")
    print(json.dumps(response_data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
