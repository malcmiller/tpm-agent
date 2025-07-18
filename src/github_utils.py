from enum import Enum
from github import Github
from github.Issue import Issue
import sys

class GithubEvent(Enum):
    ISSUE = "issues"
    ISSUE_COMMENT = "issue_comment"

class GithubLabel(Enum):
    VSWE_ASSIGN = "vswe-assign"
    VTPM_REVIEW = "vtpm-review"
    VTPM_IGNORE = "vtpm-ignore"

def has_label(issue: Issue, label_name: str) -> bool:
    """
    Check if a GitHub issue has a label with the given name (case-insensitive).

    Args:
        issue (Issue.Issue): The GitHub issue object.
        label_name (str): The label name to check for.

    Returns:
        bool: True if the label exists, False otherwise.
    """
    if not hasattr(issue, "labels") or not isinstance(issue.labels, list):
        return False
    return any(getattr(label, "name", "").lower() == label_name.lower() for label in issue.labels)

def get_github_issue(token: str, repository: str, issue_id: int) -> Issue:
    """
    Fetch a GitHub issue by its ID.

    Args:
        token (str): GitHub access token.
        repository (str): Repository in 'owner/name' format.
        issue_id (int): The issue number.

    Returns:
        Issue.Issue: The fetched GitHub issue object.

    Raises:
        SystemExit: If the repository or issue cannot be found or accessed.
    """
    try:
        github_client = Github(token)
        repo = github_client.get_repo(repository)
        issue = repo.get_issue(issue_id)
        return issue
    except Exception as e:
        print(f"Error fetching GitHub issue: {e}", file=sys.stderr)
        sys.exit(1)


def create_github_issue_comment(issue: Issue, comment: str) -> bool:
    """
    Create a comment on a GitHub issue with detailed error reporting.

    Args:
        issue (Issue): The GitHub issue object.
        comment (str): The comment text to post.

    Returns:
        bool: True if the comment was created successfully, False otherwise.
    """
    try:
        issue.create_comment(comment)
        return True
    except Exception as e:
        print(f"Error creating GitHub issue comment: {type(e).__name__}: {e}", file=sys.stderr)
        return False