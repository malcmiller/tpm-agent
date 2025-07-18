from github import Github, Issue

def get_github_issue(token: str, repository: str, issue_id: int) -> Issue.Issue:
    """Fetch a GitHub issue by its ID."""

    github_client = Github(token)
    repo = github_client.get_repo(repository)
    issue = repo.get_issue(issue_id)
    return issue
    
