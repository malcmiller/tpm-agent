from github_utils import get_github_issue, has_label, GithubLabel
from openai_utils import initialize_kernel
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
    azure_openai_target_uri = get_env_var("INPUT_AZURE_OPENAI_TARGET_URI")
    azure_openai_api_key = get_env_var("INPUT_AZURE_OPENAI_API_KEY")
    repository = get_env_var("GITHUB_REPOSITORY")

    github_issue = get_github_issue(
        token=github_token, repository=repository, issue_id=github_issue_id
    )

    if check_all and has_label(github_issue, GithubLabel.VTPM_IGNORE.value):
        print(f"Issue {github_issue_id} is ignored due to label {GithubLabel.VTPM_IGNORE.value}.")
        return
    
    if not check_all and not has_label(github_issue, GithubLabel.VTPM_REVIEW.value):
        print(f"Issue {github_issue_id} does not require review due to missing label {GithubLabel.VTPM_REVIEW.value}.")
        return

    print(f"Processing issue: {github_issue.title}")
    print(f"Event Name: {github_event_name}, Action: {github_event_action}")


    # Initialize the Semantic Kernel with Azure OpenAI
    kernel = initialize_kernel(
        azure_openai_target_uri=azure_openai_target_uri,
        azure_openai_api_key=azure_openai_api_key,
    )

if __name__ == "__main__":
    main()
