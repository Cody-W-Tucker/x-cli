"""
Get Events by Conversation ID - X API v2
=========================================
Endpoint: GET https://api.x.com/2/dm_conversations/:dm_conversation_id/dm_events
Docs: https://developer.x.com/en/docs/twitter-api/direct-messages/lookup/api-reference/get-dm-conversations-dm_conversation_id-dm_events

Authentication: OAuth 2.0 (User Context)
Required env vars: CLIENT_ID, CLIENT_SECRET

This example retrieves Direct Message events by conversation ID.
This supports both one-to-one and group conversations.
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
scopes = ["dm.read", "tweet.read", "users.read", "offline.access"]

# What is the ID of the conversation to retrieve?
dm_conversation_id = "1512210732774948865"

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
    
    # Step 6: Get events by conversation ID with automatic pagination
    all_events = []
    for page in client.direct_messages.get_events_by_conversation_id(
        dm_conversation_id,
        max_results=100
    ):
        # Access data attribute (model uses extra='allow' so data should be available)
        # Use getattr with fallback in case data field is missing from response
        page_data = getattr(page, 'data', []) or []
        all_events.extend(page_data)
        print(f"Fetched {len(page_data)} events (total: {len(all_events)})")
    
    print(f"\nTotal Conversation Events: {len(all_events)}")
    print(json.dumps({"data": all_events[:5]}, indent=4, sort_keys=True))  # Print first 5 as example

if __name__ == "__main__":
    main()
