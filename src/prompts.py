from typing import Dict

SYSTEM_PROMPT = "You are a helpful assistant that analyzes and improves GitHub issues using natural language."

def build_user_story_eval_prompt(issue_title: str, issue_body: str) -> list:
    prompt = (
        f"## GitHub Issue Context\n"
        f"Title: {issue_title}\n"
        f"Body: {issue_body}\n\n"

        "## Evaluation Instructions\n"
        "Assess the issue as a candidate user story for engineering work. Your response must:\n"
        "1. Provide a concise, AI-enhanced summary or insight about the story.\n"
        "2. Confirm the presence of the following elements (respond only with 'Yes' or 'No'):\n"
        "   - Title\n"
        "   - Description\n"
        "   - Acceptance Criteria\n"
        "3. Judge the clarity and completeness of the description. Does it convey why the story matters (business value, user need, technical dependency)?\n"
        "4. Analyze the acceptance criteria for clarity, specificity, and testability via automation.\n"
        "   - If not automatable, include a warning and suggest improvements.\n"
        "5. Suggest up to 3 relevant GitHub labels (e.g. 'bug', 'enhancement', 'good first issue'). Format as a comma-separated list.\n"
        "6. Render a Boolean judgment: Is this story 'Ready to Work'? Criteria: all elements present, clear purpose, and testable acceptance criteria.\n\n"

        "⚠️ If the title or description is vague, placeholder-like, or lacks meaningful value (e.g. 'Test', 'TBD', 'No update provided'), then:\n"
        "   Base Story Not Clear: True\n"
        "   Ready to Work: False\n"
        "   Skip the 'Refactored Story' section entirely.\n\n"
        "🟢 If Ready to Work is True, also skip the 'Refactored Story' section.\n\n"

        "## Expected Response Format\n"
        "### Evaluation\n"
        "Summary: <your insight>\n"
        "Completeness:\n"
        " - Title: Yes\n"
        " - Description: Yes\n"
        " - Acceptance Criteria: No\n"
        "Importance: <why it matters>\n"
        "Acceptance Criteria Evaluation: <analysis + any testability warning>\n"
        "Labels: <comma-separated label list>\n"
        "Ready to Work: <True/False>\n"
        "Base Story Not Clear: <True/False>\n\n"

        "### Refactored Story\n"
        "(Include this section only if Ready to Work is False AND Base Story Not Clear is False. Always return a full version of the user story — even if only one part needed editing.)\n"
        "Title: <refined title>\n"
        "Description: <expanded explanation with business value or user need>\n"
        "Acceptance Criteria:\n"
        "- <criterion one>\n"
        "- <criterion two>\n"
        "- <etc...>\n"
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
