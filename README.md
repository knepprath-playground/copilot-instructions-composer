# Create a GitHub App

- Go to GitHub settings and create a new GitHub App.
- Set the necessary permissions (e.g., read and write access to repository contents, read access to repository metadata).
- Generate a private key for the app.
- Set the webhook URL to a placeholder (you will update this later with your server URL).
- Subscribe to the push event.


# Environment Variables
Set the following environment variables:

- GITHUB_APP_ID
- GITHUB_PRIVATE_KEY (Base64 encoded private key)
- GITHUB_WEBHOOK_SECRET

# Deploy the Server

`pip install flask pygithub requests`

`python server.py`

Update the webhook URL in your GitHub App settings to point to your server's public IP or domain name.

# Integration Setup

Define a repo as source of truth with a copilot-instructions.md

Add the `copilot` topic to a repo in the org

After the github app has been fully set up then push a change to the copilot-instructions.md 
