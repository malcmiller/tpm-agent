from typing import Optional, List

class UserStorySuggestions:
    """
    Model for the Suggestions section in the AI response.
    """
    def __init__(self, title: str = "", description: str = "", acceptance_criteria: Optional[List[str]] = None):
        self.title = title
        self.description = description
        self.acceptance_criteria = acceptance_criteria or []

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            acceptance_criteria=data.get("acceptance_criteria", []),
        )

    def to_markdown(self) -> str:
        lines = []
        if self.title:
            lines.append(f"Title: {self.title}")
        if self.description:
            lines.append(f"Description: {self.description}")
        if self.acceptance_criteria:
            lines.append("Acceptance Criteria:")
            for criterion in self.acceptance_criteria:
                lines.append(f"- {criterion}")
        return "\n".join(lines)

class UserStoryEvalResponse:
    """
    Model for parsing and representing the AI response from the user story evaluation prompt.
    """
    def __init__(
        self,
        summary: str,
        title_complete: bool,
        description_complete: bool,
        acceptance_criteria_complete: bool,
        importance: str,
        acceptance_criteria_evaluation: str,
        labels: List[str],
        ready_to_work: bool,
        base_story_not_clear: bool,
        suggestions: Optional[UserStorySuggestions] = None,
    ):
        self.summary = summary
        self.title_complete = title_complete
        self.description_complete = description_complete
        self.acceptance_criteria_complete = acceptance_criteria_complete
        self.importance = importance
        self.acceptance_criteria_evaluation = acceptance_criteria_evaluation
        self.labels = labels
        self.ready_to_work = ready_to_work
        self.base_story_not_clear = base_story_not_clear
        self.suggestions = suggestions or UserStorySuggestions()

    @classmethod
    def from_text(cls, text: str):
        """
        Parse the AI response text and return a UserStoryEvalResponse instance.
        """
        # Basic parsing logic (can be improved for edge cases)
        def extract_bool(line):
            return line.strip().split(":")[-1].strip().lower() == "true"
        def extract_yesno(line):
            return line.strip().split(":")[-1].strip().lower() == "yes"
        lines = text.splitlines()
        summary = ""
        title_complete = False
        description_complete = False
        acceptance_criteria_complete = False
        importance = ""
        acceptance_criteria_evaluation = ""
        labels = []
        ready_to_work = False
        base_story_not_clear = False
        suggestions_dict = {}
        section = None
        for line in lines:
            if line.startswith("Summary:"):
                summary = line.split(":", 1)[-1].strip()
            elif line.strip().startswith("- Title:"):
                title_complete = extract_yesno(line)
            elif line.strip().startswith("- Description:"):
                description_complete = extract_yesno(line)
            elif line.strip().startswith("- Acceptance Criteria:"):
                acceptance_criteria_complete = extract_yesno(line)
            elif line.startswith("Importance:"):
                importance = line.split(":", 1)[-1].strip()
            elif line.startswith("Acceptance Criteria Evaluation:"):
                acceptance_criteria_evaluation = line.split(":", 1)[-1].strip()
            elif line.startswith("Labels:"):
                labels = [l.strip() for l in line.split(":", 1)[-1].split(",") if l.strip()]
            elif line.startswith("Ready to Work:"):
                ready_to_work = extract_bool(line)
            elif line.startswith("Base Story Not Clear:"):
                base_story_not_clear = extract_bool(line)
            elif line.startswith("### Suggestions"):
                section = "suggestions"
            elif section == "suggestions":
                if line.startswith("Title:"):
                    suggestions_dict["title"] = line.split(":", 1)[-1].strip()
                elif line.startswith("Description:"):
                    suggestions_dict["description"] = line.split(":", 1)[-1].strip()
                elif line.startswith("Acceptance Criteria:"):
                    suggestions_dict["acceptance_criteria"] = []
                elif line.startswith("-"):
                    if "acceptance_criteria" in suggestions_dict:
                        suggestions_dict["acceptance_criteria"].append(line.lstrip("- ").strip())
        return cls(
            summary,
            title_complete,
            description_complete,
            acceptance_criteria_complete,
            importance,
            acceptance_criteria_evaluation,
            labels,
            ready_to_work,
            base_story_not_clear,
            UserStorySuggestions.from_dict(suggestions_dict),
        )

    def to_markdown(self) -> str:
        def yn_emoji(val: bool) -> str:
            return "✅" if val else "❌"
        lines = [
            "### Evaluation",
            f"Summary: {self.summary}",
            "Completeness:",
            f" - Title: {yn_emoji(self.title_complete)}",
            f" - Description: {yn_emoji(self.description_complete)}",
            f" - Acceptance Criteria: {yn_emoji(self.acceptance_criteria_complete)}",
            f"Importance: {self.importance}",
            f"Acceptance Criteria Evaluation: {self.acceptance_criteria_evaluation}",
            f"Labels: {', '.join(self.labels)}",
            f"Ready to Work: {yn_emoji(self.ready_to_work)}",
        ]
 
        if not self.ready_to_work and self.base_story_not_clear:
            lines.append(
                "\n**❌ Suggestions could not be provided because the original story is unclear or lacks meaningful value. Please rewrite the title and description to clearly explain the story's purpose and value.**"
            )
            
        if self.suggestions and (not self.ready_to_work and not self.base_story_not_clear):
            lines.append("\n### Suggestions")
            lines.append(self.suggestions.to_markdown())
        return "\n".join(lines)
