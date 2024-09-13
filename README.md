# LocalStashClean

`LocalStashClean.py` is a Python script that performs a metadata cleanup on a local Stash server via a GraphQL mutation. It also sends notifications to Uptime Kuma to monitor the success or failure of the cleanup operation. This script supports an optional dry-run mode, where it simulates the cleanup without actually performing it.

## Prerequisites

1. **Python 3.x**
2. **Python Packages**:

   - `requests`
   - `python-dotenv`

   You can install these dependencies by running:

   ```bash
   pip install requests python-dotenv
   ```

3. **Stash Server**: A running instance of Stash with GraphQL enabled.
4. **Uptime Kuma**: A configured instance of Uptime Kuma to receive notifications.

## Setup

1. Clone or download the script.
2. Create a `.env` file in the same directory as the script with the following environment variables:

   ```bash
   STASH_BASEURL=http://local.stash.instance.lan   # Base URL of your Stash instance
   STASH_APIKEY=your-stash-api-key   # API key for Stash authentication
   CLEAN_PATH=/path/to/stash          # Path to the directory to be cleaned
   UPTIME_KUMA_URL=https://uptimekuma.instance.lan/api/push/{monitorId}  # URL to send notifications to Uptime Kuma
   ```

   - **STASH_BASEURL**: The base URL of your Stash instance (e.g., `http://local.stash.instance.lan`).
   - **STASH_APIKEY**: The API key for authenticating with your Stash server.
   - **CLEAN_PATH**: The directory path where your Stash videos are stored.
   - **UPTIME_KUMA_URL**: The URL of your Uptime Kuma API for sending notifications.

## Usage

You can run the script with or without the `--dry-run` flag:

1. **Run the script (actual clean)**:

   This will trigger the `metadataClean` mutation on the Stash server and notify Uptime Kuma of success or failure.

   ```bash
   python LocalStashClean.py
   ```

2. **Run the script with dry-run**:

   This will perform a dry run where no actual metadata cleanup is performed. However, Uptime Kuma will still receive notifications based on the result.

   ```bash
   python LocalStashClean.py --dry-run
   ```

### Script Arguments

- `--dry-run`: Use this flag to simulate the cleanup without actually deleting or modifying metadata.

## Notifications

- If the metadata clean operation is successful, a notification with the status `up` and message `Metadata clean successful` will be sent to Uptime Kuma.
- If the operation fails, a notification with the status `down` and the corresponding error message will be sent to Uptime Kuma.

## Example .env File

```bash
STASH_BASEURL=http://local.stash.instance.lan
STASH_APIKEY=stash-api-key
CLEAN_PATH=/path/to/stash
UPTIME_KUMA_URL=https://uptimekuma.instance.lan/api/push/{monitorId}
```

## Error Handling

- If the GraphQL query fails or there is an issue with the Stash server, the script will notify Uptime Kuma with a `down` status and display the error message.
- In case of a successful run, Uptime Kuma will be notified with an `up` status.

## License

This script is open source and free to use under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Feel free to submit issues or contribute by opening a pull request on the GitHub repository.

---

### Key Points

- **Prerequisites**: Lists required tools and libraries.
- **Setup**: Explains how to configure the environment and run the script.
- **Usage**: Describes how to run the script, including using the `--dry-run` argument.
- **Notifications**: Clarifies the success/failure notification system with Uptime Kuma.
- **Error Handling**: Brief explanation of what happens in case of errors.
