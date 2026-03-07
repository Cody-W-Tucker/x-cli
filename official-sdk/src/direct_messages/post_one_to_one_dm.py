"""
Post One-to-One Direct Message - X API v2
==========================================
Endpoint: POST https://api.x.com/2/dm_conversations/with/:participant_id/messages
Docs: https://developer.x.com/en/docs/twitter-api/direct-messages/manage/api-reference/post-dm-conversations-with-participant_id-messages

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
scopes = ["dm.read", "dm.write", "tweet.read", "users.read", "offline.access"]

# Who is this DM being sent to? Reference their User ID.
participant_id = "1716450569358098432"

# Set the text of the message to be sent.
text_message = "Hi, I am DMing you using the v2 DM one-to-one endpoint."

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
    
    # Step 6: Send one-to-one DM
    payload = {"text": text_message}
    response = client.direct_messages.create_by_participant_id(participant_id, body=payload)
    
    print("Response code: 201")
    print(json.dumps(response.data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
