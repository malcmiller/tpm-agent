from github_utils import get_github_issue, GithubLabel
from utils import get_env_var


def main() -> None:
    """Main entry point for the issue enhancer agent."""

    check_all = get_env_var(
        "INPUT_CHECK_ALL",
        required=False,
        cast_func=lambda v: str(v).strip().lower() in ["1", "true", "yes"],
        default=False,
    )
    github_event_name = get_env_var("INPUT_GITHUB_EVENT_NAME")
    github_event_action = get_env_var("INPUT_GITHUB_EVENT_ACTION")
    github_issue_id = get_env_var("INPUT_GITHUB_ISSUE_ID", cast_func=int)
    github_token = get_env_var("INPUT_GITHUB_TOKEN")
    azure_openai_endpoint = get_env_var("INPUT_AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment = get_env_var("INPUT_AZURE_OPENAI_DEPLOYMENT")
    azure_openai_api_key = get_env_var("INPUT_AZURE_OPENAI_API_KEY")
    repository = get_env_var("GITHUB_REPOSITORY")

    github_issue = get_github_issue(
        token=github_token, repository=repository, issue_id=github_issue_id
    )

    if check_all and GithubLabel.VTPM_IGNORE.value in github_issue.labels:
        print(f"Issue {github_issue_id} is ignored due to label {GithubLabel.VTPM_IGNORE.value}.")
        return
    
    if not check_all and GithubLabel.VTPM_REVIEW.value not in github_issue.labels:
        print(f"Issue {github_issue_id} does not require review due to missing label {GithubLabel.VTPM_REVIEW.value}.")
        return

    print(f"Processing issue: {github_issue.title}")
    print(f"Event Name: {github_event_name}, Action: {github_event_action}")


if __name__ == "__main__":
    main()
