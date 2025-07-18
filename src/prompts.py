from typing import Dict

SYSTEM_PROMPT = "You are a helpful assistant that analyzes and improves GitHub issues using natural language."

def build_user_story_eval_prompt(issue_title: str, issue_body: str) -> list:
    prompt = (
        f"## GitHub Issue Context\n"
        f"Title: {issue_title}\n"
        f"Body: {issue_body}\n\n"
        "## Evaluation Instructions\n"
        "Evaluate this issue as a potential user story for engineering work.\n"
        "In your response:\n"
        "1. Provide an AI-enhanced summary or insight about the story.\n"
        "2. Confirm whether the following elements are present. Only respond with 'Yes' or 'No' for each item:\n"
        "   - A title\n"
        "   - A description\n"
        "   - Acceptance criteria\n"
        "3. Evaluate the clarity and completeness of the description. Does it explain why the story matters (e.g. business value, customer need, technical dependency)?\n"
        "4. Analyze the acceptance criteria. Are they clear, specific, and testable via automated testing?\n"
        "   - If you believe the acceptance criteria are not automatable, provide a warning with suggestions for making them testable.\n"
        "5. Suggest up to 3 relevant GitHub labels (such as 'bug', 'good first issue', 'enhancement', etc.) as a comma-separated list.\n"
        "6. Based on your analysis, provide a final Boolean judgment of whether this story is ready to be worked. Assume 'ready' means: all required elements are present, purpose is clear, and acceptance criteria are testable.\n\n"
        "⚠️ If the title or description is vague, placeholder-like, or fails to convey meaningful value (e.g. contains phrases like 'Test', 'No update provided', 'TBD'), set:\n"
        "   Base Story Not Clear: True\n"
        "   Ready to Work: False\n"
        "   Do not include the Suggestions section.\n"
        "🟢 If Ready to Work is True, skip the Suggestions section as well.\n\n"
        "## Expected Response Format\n"
        "### Evaluation\n"
        "Summary: <your insight>\n"
        "Completeness:\n"
        " - Title: Yes\n"
        " - Description: Yes\n"
        " - Acceptance Criteria: No\n"
        "Importance: <brief explanation>\n"
        "Acceptance Criteria Evaluation: <analysis + any testability warning>\n"
        "Labels: <comma-separated label list>\n"
        "Ready to Work: <True/False>\n"
        "Base Story Not Clear: <True/False>\n\n"
        "### Suggestions (only include this section if Ready to Work is False AND Base Story Not Clear is False)\n"
        "Title: <rewritten title>\n"
        "Description: <expanded explanation>\n"
        "Acceptance Criteria:\n"
        "- <criterion one>\n"
        "- <etc...>\n"
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
