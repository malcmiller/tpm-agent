from typing import Dict

SYSTEM_PROMPT = "You are a helpful assistant that analyzes and improves GitHub issues using natural language."

def build_user_story_eval_prompt(issue_title: str, issue_body: str) -> list:
    prompt = (
        f"Given the following GitHub issue:\n"
        f"Title: {issue_title}\n"
        f"Body: {issue_body}\n\n"
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
        "Format your response like this (do not include explanations in the 'Completeness' section):\n"
        "Summary: <your insight>\n"
        "Completeness:\n"
        " - Title: Yes\n"
        " - Description: Yes\n"
        " - Acceptance Criteria: No\n"
        "Importance: <Brief assessment of why the story matters>\n"
        "Acceptance Criteria Evaluation: <Analysis + any testability warning>\n"
        "Labels: <comma-separated label list>\n"
        "Ready to Work: <True/False>\n\n"
        "If any required elements are missing or not testable, provide actionable suggestions to make the story ready.\n"
        "For each missing or insufficient element, propose improvements:\n"
        " - Improved Title (if missing or unclear)\n"
        " - Expanded Description (if missing or unclear)\n"
        " - Specific and testable Acceptance Criteria (if missing or unclear)\n"
        "If you are unable to confidently generate any missing core elements, return:\n"
        "   Not Applicable: True\n\n"
        "Format your suggestions like this:\n"
        "Suggestions:\n"
        "Title: <rewritten title>\n"
        "Description: <expanded explanation>\n"
        "Acceptance Criteria:\n"
        "- <criterion one>\n"
        "- <criterion two>\n"
        "- <etc...>\n"
        "Not Applicable: <True/False>"
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
