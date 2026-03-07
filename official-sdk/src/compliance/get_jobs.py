"""
Get Compliance Jobs - X API v2
==============================
Endpoint: GET https://api.x.com/2/compliance/jobs
Docs: https://developer.x.com/en/docs/twitter-api/compliance/batch-compliance/api-reference/get-compliance-jobs

Authentication: Bearer Token (App-only)
Required env vars: BEARER_TOKEN
"""

import os
import json
from xdk import Client

bearer_token = os.environ.get("BEARER_TOKEN")
client = Client(bearer_token=bearer_token)

# Type can be "tweets" or "users"
job_type = "tweets"

def main():
    response = client.compliance.get_jobs(type=job_type)
    
    print(json.dumps(response.data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
