# Create a GitHub App

- Go to GitHub settings and create a new GitHub App.
- Set the necessary permissions (e.g., read and write access to repository contents, read access to repository metadata).
- Generate a private key for the app.
- Set the webhook URL to a placeholder (you will update this later with your server URL).
- Subscribe to the push event.
- Make sure custom instructions is enabled in your IDE: https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot#enabling-or-disabling-custom-instructions


# Environment Variables
Set the following environment variables:

- GITHUB_APP_ID
- GITHUB_PRIVATE_KEY (replace \n with \\n)
- GITHUB_WEBHOOK_SECRET

# Deploy the Server Locally

Use ngrok to set up a public URL for you local server. Grab the Forwarding URL + "/webhooks"

Update the webhook URL in your GitHub App settings to point to your server public URL.

`pip install flask pygithub requests`

`python server.py`


# Integration Setup

Define a repo as source of truth with a copilot-instructions.md (ex: https://github.com/knepprath-playground/copilot-instructions/blob/main/.github/copilot-instructions.md)

Add the `copilot` topic to a repo in the org (ex: https://github.com/knepprath-playground/test-repo-1)

After the github app has been fully set up then push a change to the copilot-instructions.md and observe that a PR is opened (ex: https://github.com/knepprath-playground/test-repo-1/pull/1)


# TODO
- Configure the Github app to use either Topics or Properties (what's githubs position on how these should be used differnelty? Is there a reason to support both?)
- Define a pattern and implement composing the instruction file from multiple tags