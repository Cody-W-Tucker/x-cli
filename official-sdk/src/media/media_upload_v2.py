"""
Media Upload v2 (Video) - X API v2
===================================
Endpoint: POST https://api.x.com/2/media/upload
Docs: https://developer.x.com/en/docs/twitter-api/media/upload-media/api-reference

Authentication: OAuth 2.0 (User Context)
Required env vars: CLIENT_ID, CLIENT_SECRET

This example demonstrates uploading a video file using chunked uploads.
"""

import os
import sys
import time
import requests
from xdk.oauth2_auth import OAuth2PKCEAuth

MEDIA_ENDPOINT_URL = 'https://api.x.com/2/media/upload'
POST_TO_X_URL = 'https://api.x.com/2/tweets'

# Replace with path to file
VIDEO_FILENAME = 'REPLACE_ME'

# The code below sets the client ID and client secret from your environment variables
# To set environment variables on macOS or Linux, run the export commands below from the terminal:
# export CLIENT_ID='YOUR-CLIENT-ID'
# export CLIENT_SECRET='YOUR-CLIENT-SECRET'
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
redirect_uri = "https://example.com"

# Set the scopes
scopes = ["media.write", "users.read", "tweet.read", "tweet.write", "offline.access"]

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
access = tokens["access_token"]

headers = {
    "Authorization": "Bearer {}".format(access),
    "Content-Type": "application/json",
    "User-Agent": "MediaUploadSampleCode",
}


class VideoPost(object):

    def __init__(self, file_name):
        # Defines video Post properties
        self.video_filename = file_name
        self.total_bytes = os.path.getsize(self.video_filename)
        self.media_id = None
        self.processing_info = None

    def upload_init(self):
        # Initializes Upload
        print('INIT')

        request_data = {
            'command': 'INIT',
            'media_type': 'video/mp4',
            'total_bytes': self.total_bytes,
            'media_category': 'tweet_video'
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL, params=request_data, headers=headers)
        print(req.status_code)
        print(req.text)
        media_id = req.json()['data']['id']

        self.media_id = media_id

        print('Media ID: %s' % str(media_id))

    def upload_append(self):
        segment_id = 0
        bytes_sent = 0
        with open(self.video_filename, 'rb') as file:
            while bytes_sent < self.total_bytes:
                chunk = file.read(4 * 1024 * 1024)  # 4MB chunk size

                print('APPEND')

                files = {'media': ('chunk', chunk, 'application/octet-stream')}

                data = {
                    'command': 'APPEND',
                    'media_id': self.media_id,
                    'segment_index': segment_id
                }

                headers = {
                    "Authorization": f"Bearer {access}",
                    "User-Agent": "MediaUploadSampleCode",
                }

                req = requests.post(url=MEDIA_ENDPOINT_URL, data=data, files=files, headers=headers)

                if req.status_code < 200 or req.status_code > 299:
                    print(req.status_code)
                    print(req.text)
                    sys.exit(0)

                segment_id += 1
                bytes_sent = file.tell()

                print(f'{bytes_sent} of {self.total_bytes} bytes uploaded')

        print('Upload chunks complete.')

    def upload_finalize(self):

        # Finalizes uploads and starts video processing
        print('FINALIZE')

        request_data = {
            'command': 'FINALIZE',
            'media_id': self.media_id
        }

        req = requests.post(url=MEDIA_ENDPOINT_URL, params=request_data, headers=headers)

        print(req.json())

        self.processing_info = req.json()['data'].get('processing_info', None)
        self.check_status()

    def check_status(self):
        # Checks video processing status
        if self.processing_info is None:
            return

        state = self.processing_info['state']

        print('Media processing status is %s ' % state)

        if state == u'succeeded':
            return

        if state == u'failed':
            sys.exit(0)

        check_after_secs = self.processing_info['check_after_secs']

        print('Checking after %s seconds' % str(check_after_secs))
        time.sleep(check_after_secs)

        print('STATUS')

        request_params = {
            'command': 'STATUS',
            'media_id': self.media_id
        }

        req = requests.get(url=MEDIA_ENDPOINT_URL, params=request_params, headers=headers)

        self.processing_info = req.json()['data'].get('processing_info', None)
        self.check_status()

    def post(self):

        # Publishes Post with attached video
        payload = {
            'text': 'I just uploaded a video with the media upload v2 @XDevelopers API.',
            'media': {
                'media_ids': [self.media_id]
            }
        }

        req = requests.post(url=POST_TO_X_URL, json=payload, headers=headers)

        print(req.json())


if __name__ == '__main__':
    videoPost = VideoPost(VIDEO_FILENAME)
    videoPost.upload_init()
    videoPost.upload_append()
    videoPost.upload_finalize()
    videoPost.post()
