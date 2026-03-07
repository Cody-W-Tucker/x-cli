"""
Download Compliance Results - X API v2
======================================
Endpoint: GET <download_url> (provided in compliance job response)
Docs: https://developer.x.com/en/docs/twitter-api/compliance/batch-compliance/api-reference/get-compliance-jobs-id

Note: This endpoint uses a pre-signed URL from the compliance job response.
The download_url is provided when you check the status of a compliance job.
"""

import requests

# Replace with your job download_url (from the compliance job response)
download_url = ''

def main():
    response = requests.get(download_url)
    
    print(f"Response code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    entries = response.text.splitlines()
    for entry in entries:
        print(entry)

if __name__ == "__main__":
    main()
