import asyncio
import sys

from github.Issue import Issue
from semantic_kernel import Kernel

from github_utils import GithubEvent, GithubLabel, get_github_issue, has_label
from openai_utils import initialize_kernel, run_completion
from prompts import build_user_story_eval_prompt
from utils import get_env_var
from response_models import UserStoryEvalResponse


def handle_github_issues_event(issue: Issue, kernel: Kernel) -> None:
    messages = build_user_story_eval_prompt(issue.title, issue.body)

    # Run completion
    try:
        response_text = asyncio.run(run_completion(kernel, messages))
        response = UserStoryEvalResponse.from_text(response_text)
        print(f"AI Response for Issue {issue.number} (Markdown):\n\n{response.to_markdown()}")
    except Exception as e:
        print(f"Error running Azure OpenAI completion: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the issue enhancer agent."""

    check_all = get_env_var(
        "INPUT_CHECK_ALL",
        required=False,
        cast_func=lambda v: str(v).strip().lower() in ["1", "true", "yes"],
        default=False,
    )
    github_event_name = get_env_var("INPUT_GITHUB_EVENT_NAME")
    github_issue_id = get_env_var("INPUT_GITHUB_ISSUE_ID", cast_func=int)
    github_token = get_env_var("INPUT_GITHUB_TOKEN")
    azure_openai_target_uri = get_env_var("INPUT_AZURE_OPENAI_TARGET_URI")
    azure_openai_api_key = get_env_var("INPUT_AZURE_OPENAI_API_KEY")
    repository = get_env_var("GITHUB_REPOSITORY")

    if github_event_name not in [e.value for e in GithubEvent]:
        print(f"Error: Unsupported GitHub event: {github_event_name}", file=sys.stderr)
        sys.exit(1)

    github_issue = get_github_issue(
        token=github_token, repository=repository, issue_id=github_issue_id
    )

    if check_all and has_label(github_issue, GithubLabel.VTPM_IGNORE.value):
        print(
            f"Issue {github_issue_id} is ignored due to label {GithubLabel.VTPM_IGNORE.value}."
        )
        return

    if not check_all and not has_label(github_issue, GithubLabel.VTPM_REVIEW.value):
        print(
            f"Issue {github_issue_id} does not require review due to missing label {GithubLabel.VTPM_REVIEW.value}."
        )
        return

    print(f"Processing issue: {github_issue.title}")
    print(f"Event Name: {github_event_name}")

    # Initialize the Semantic Kernel with Azure OpenAI
    kernel = initialize_kernel(
        azure_openai_target_uri=azure_openai_target_uri,
        azure_openai_api_key=azure_openai_api_key,
    )

    if github_event_name == GithubEvent.ISSUE.value:
        handle_github_issues_event(github_issue, kernel)
    else:
        print(f"Unsupported GitHub event: {github_event_name}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
