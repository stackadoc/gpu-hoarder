# GPU Hoarder

## Description

GPU Hoarder is a Python project designed to monitor the availability of GPUs across multiple cloud platforms. 
It notifies users when a GPU becomes available, helping to streamline the process of acquiring computing resources.

## Installation

### Prerequisites
- Python 3.x
- pip

### Steps
1. Clone the repository:
   ```bash
   git clone git@github.com:stackadoc/gpu-hoarder.git
   ```
2. Navigate to the project directory:
   ```bash
   cd gpu-hoarder
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables
To configure GPU Hoarder, set the following environment variables:

- `SCALEWAY_SECRET_KEY`: Your Scaleway API secret key.
- `SCALEWAY_ENABLED`: Set to `true` to enable monitoring on Scaleway.
- `SCALEWAY_ZONES`: Comma-separated list of zones to monitor in Scaleway.
- `SCALEWAY_INSTANCES_TYPES`: Comma-separated list of instance types to monitor in Scaleway.
- `SLACK_ENABLED`: Set to `true` to enable Slack notifications.
- `SLACK_TOKEN`: Your Slack API token.
- `SLACK_CHANNEL`: The Slack channel where notifications will be sent.
- `SLEEP`: Time in seconds between checks.
- `NOTIFY_NEW_INSTANCES`: Set to `true` to receive notifications for new instances.
- `NOTIFY_LOST_INSTANCES`: Set to `true` to receive notifications for lost instances.

### Setting up the `.env` file
Create a `.env` file in the root directory and populate it with the necessary environment variables:
```plaintext
SCALEWAY_SECRET_KEY=your_scaleway_api_key
SCALEWAY_ENABLED=true
SCALEWAY_ZONES=fr-par-1,fr-par-2
SCALEWAY_INSTANCES_TYPES=GP1-S,GP1-M
SLACK_ENABLED=true
SLACK_TOKEN=your_slack_token
SLACK_CHANNEL=your_slack_channel
SLEEP=300
NOTIFY_NEW_INSTANCES=true
NOTIFY_LOST_INSTANCES=true
```

Contributions to improve the project are welcome. Please ensure to follow the best practices and coding standards.
