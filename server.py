import os
import hmac
import hashlib
from flask import Flask, request, abort
from github import Github, GithubIntegration

app = Flask(__name__)

# GitHub App credentials
APP_ID = os.getenv('GITHUB_APP_ID')
PRIVATE_KEY = os.getenv('GITHUB_PRIVATE_KEY').replace('\\n', '\n')
WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')

# Initialize GitHub integration
integration = GithubIntegration(APP_ID, PRIVATE_KEY)

# Repository and file details
GITHUB_ORG = 'knepprath-playground'
SOURCE_REPO = 'knepprath-playground/copilot-instructions'
FILE_PATH = '.github/copilot-instructions.md'
TARGET_TOPIC = 'copilot'

@app.route('/webhooks', methods=['POST'])
def webhooks():
    app.logger.info('Webhook received')

    # Verify webhook signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not is_valid_signature(request.data, signature):
        app.logger.error('Invalid signature')
        abort(401, 'Invalid signature')

    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    if event == 'push' and payload['repository']['full_name'] == SOURCE_REPO:
        handle_push_event(payload)

    return 'Event received', 200

def is_valid_signature(payload, signature):
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = f'sha256={mac.hexdigest()}'
    return hmac.compare_digest(expected_signature, signature)

def handle_push_event(payload):
    commits = payload['commits']
    file_updated = any(FILE_PATH in commit['modified'] for commit in commits)

    if file_updated:
        installation_id = payload['installation']['id']
        github = Github(integration.get_access_token(installation_id).token)

        source_repo = github.get_repo(SOURCE_REPO)
        file_content = source_repo.get_contents(FILE_PATH).decoded_content.decode()

        org = github.get_organization(GITHUB_ORG)
        for repo in org.get_repos():
            if TARGET_TOPIC in repo.get_topics():
                create_or_update_pull_request(repo, file_content)

def create_or_update_pull_request(repo, file_content):
    branch_name = 'update-copilot-instructions'
    base_branch = repo.default_branch

    # Create a new branch or update the existing branch
    try:
        source = repo.get_branch(base_branch)
        repo.create_git_ref(ref=f'refs/heads/{branch_name}', sha=source.commit.sha)
    except:
        # Branch already exists, update the reference
        ref = repo.get_git_ref(f'heads/{branch_name}')
        base_commit = repo.get_branch(base_branch).commit.sha
        ref.edit(sha=base_commit, force=True)

    # Create or update the file
    try:
        contents = repo.get_contents(FILE_PATH, ref=branch_name)
        repo.update_file(contents.path, 'Update copilot-instructions.md', file_content, contents.sha, branch=branch_name)
    except:
        repo.create_file(FILE_PATH, 'Add copilot-instructions.md', file_content, branch=branch_name)

    # Create a pull request
    try:
        repo.create_pull(title='Update copilot-instructions.md', body='This PR updates the copilot-instructions.md file.', head=branch_name, base=base_branch)
    except:
        # Pull request already exists, update it if necessary
        pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
