import requests
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

STASH_BASEURL = os.getenv("STASH_BASEURL")
STASH_APIKEY = os.getenv("STASH_APIKEY")
CLEAN_PATH = os.getenv("CLEAN_PATH")
UPTIME_KUMA_URL = os.getenv("UPTIME_KUMA_URL")

# Function to send requests to Uptime Kuma
def notify_uptime_kuma(status, msg=""):
    url = f"{UPTIME_KUMA_URL}?status={status}&msg={msg}&ping="
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Notification sent to Uptime Kuma: {status} - {msg}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to notify Uptime Kuma: {e}")

# Function to execute the metadataClean mutation
def clean_metadata(dry_run):
    headers = {
        "ApiKey": STASH_APIKEY,
        "Content-Type": "application/json"
    }
    graphql_query = '''
        mutation MetadataClean($paths: [String!], $dryRun: Boolean!) {
            metadataClean(input: { paths: $paths, dryRun: $dryRun })
        }
    '''
    variables = {
        "paths": CLEAN_PATH,
        "dryRun": dry_run
    }

    try:
        response = requests.post(
            f"{STASH_BASEURL}/graphql",
            json={"query": graphql_query, "variables": variables},
            headers=headers
        )
        response.raise_for_status()
        json_data = response.json()

        # Check if there were errors in the GraphQL response
        if "errors" in json_data:
            raise Exception(json_data["errors"])

        print("Metadata clean successful.")
        notify_uptime_kuma(status="up", msg="Metadata clean successful")
    except Exception as e:
        print(f"Metadata clean failed: {e}")
        notify_uptime_kuma(status="down", msg=f"Metadata clean failed: {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Clean metadata with an optional dry run.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run instead of actually cleaning the metadata."
    )
    args = parser.parse_args()

    clean_metadata(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
