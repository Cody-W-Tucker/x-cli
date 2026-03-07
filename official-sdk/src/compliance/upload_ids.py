"""
Upload IDs for Compliance Job - X API v2
========================================
Endpoint: PUT <upload_url> (provided in compliance job response)
Docs: https://developer.x.com/en/docs/twitter-api/compliance/batch-compliance/api-reference/post-compliance-jobs

Note: This endpoint uses a pre-signed URL from the compliance job response.
The upload_url is provided when you create a compliance job.
"""

import os
import requests

# Replace with your job upload_url (from the compliance job response)
upload_url = ''

# Replace with your file path that contains the list of Tweet IDs or User IDs, one ID per line
file_path = ''

def main():
    headers = {'Content-Type': "text/plain"}
    
    with open(file_path, 'rb') as f:
        response = requests.put(upload_url, data=f, headers=headers)
    
    print(f"Response code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    print(response.text)

if __name__ == "__main__":
    main()
