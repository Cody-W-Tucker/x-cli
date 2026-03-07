"""
Muted Users Lookup - X API v2
=============================
Endpoint: GET https://api.x.com/2/users/:id/muting
Docs: https://developer.x.com/en/docs/twitter-api/users/mutes/api-reference/get-users-muting

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
scopes = ["tweet.read", "users.read", "offline.access", "mute.read"]

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
    
    # Step 6: Get the authenticated user's ID
    me_response = client.users.get_me()
    user_id = me_response.data["id"]
    
    # Step 7: Get muted users with automatic pagination
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    all_users = []
    try:
        for page in client.users.get_muting(
            user_id,
            max_results=100,
            user_fields=["created_at", "description"]
        ):
            # Access data attribute (model uses extra='allow' so data should be available)
            # Use getattr with fallback in case data field is missing from response
            page_data = getattr(page, 'data', []) or []
            all_users.extend(page_data)
            print(f"Fetched {len(page_data)} users (total: {len(all_users)})")
        
        print(f"\nTotal Muted Users: {len(all_users)}")
        print(json.dumps({"data": all_users[:5]}, indent=4, sort_keys=True))  # Print first 5 as example
    except HTTPError as e:
        print(f"Error occurred: {e}")
        if hasattr(e.response, 'json'):
            try:
                error_data = e.response.json()
                if 'errors' in error_data:
                    print("Detailed errors:")
                    print(json.dumps(error_data['errors'], indent=2))
            except:
                pass
        raise

if __name__ == "__main__":
    main()