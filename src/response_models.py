from typing import Optional, List

class UserStorySuggestions:
    """
    Model for the Refactored Story section in the AI response.
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

    @classmethod
    def from_markdown(cls, markdown: str):
        """
        Parse a markdown string and return a UserStorySuggestions instance.
        """
        title = ""
        description = ""
        acceptance_criteria = []
        lines = markdown.splitlines()
        section = None
        for line in lines:
            if line.strip().startswith("Title:"):
                title = line.split(":", 1)[-1].strip()
            elif line.strip().startswith("Description:"):
                description = line.split(":", 1)[-1].strip()
            elif line.strip().startswith("Acceptance Criteria:"):
                section = "acceptance_criteria"
            elif section == "acceptance_criteria" and line.strip().startswith("-"):
                acceptance_criteria.append(line.lstrip("- ").strip())
            elif section == "acceptance_criteria" and not line.strip().startswith("-"):
                section = None
        return cls(title=title, description=description, acceptance_criteria=acceptance_criteria)

    def to_markdown(self) -> str:
        lines = []
        if self.title:
            lines.append(f"**Title**: {self.title}\n\n")
        if self.description:
            lines.append(f"**Description**: {self.description}\n\n")
        if self.acceptance_criteria:
            lines.append("**Acceptance Criteria**:")
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
            elif line.startswith("### Refactored Story"):
                section = "refactored"
            elif section == "refactored":
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

    @classmethod
    def from_markdown(cls, markdown: str):
        """
        Parse a markdown string and return a UserStoryEvalResponse instance.
        """
        def emoji_to_bool(val: str) -> bool:
            return val.strip() == "✅"
        lines = markdown.splitlines()
        summary = ""
        title_complete = False
        description_complete = False
        acceptance_criteria_complete = False
        importance = ""
        acceptance_criteria_evaluation = ""
        labels = []
        ready_to_work = False
        base_story_not_clear = False
        suggestions_md = []
        in_refactored = False
        for line in lines:
            if line.startswith("**Summary**:"):
                summary = line.split(":", 1)[-1].strip()
            elif line.strip().startswith("- Title:"):
                title_complete = emoji_to_bool(line.split(":", 1)[-1].strip())
            elif line.strip().startswith("- Description:"):
                description_complete = emoji_to_bool(line.split(":", 1)[-1].strip())
            elif line.strip().startswith("- Acceptance Criteria:"):
                acceptance_criteria_complete = emoji_to_bool(line.split(":", 1)[-1].strip())
            elif line.startswith("**Importance**:"):
                importance = line.split(":", 1)[-1].strip()
            elif line.startswith("**Acceptance Criteria Evaluation**:"):
                acceptance_criteria_evaluation = line.split(":", 1)[-1].strip()
            elif line.startswith("**Suggested Labels**:"):
                labels = [l.strip() for l in line.split(":", 1)[-1].split(",") if l.strip()]
            elif line.startswith("**Ready to Work**:"):
                ready_to_work = emoji_to_bool(line.split(":", 1)[-1].strip())
            elif "Base Story Not Clear:" in line:
                base_story_not_clear = emoji_to_bool(line.split(":", 1)[-1].strip())
            elif "could not be provided because the original story is unclear" in line:
                base_story_not_clear = True
            elif line.strip().startswith("### Refactored Story"):
                in_refactored = True
            elif in_refactored:
                suggestions_md.append(line)
        suggestions = UserStorySuggestions.from_markdown("\n".join(suggestions_md)) if suggestions_md else None
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
            suggestions,
        )

    def to_markdown(self) -> str:
        def yn_emoji(val: bool) -> str:
            return "✅" if val else "❌"
        lines = [
            "### 🤖 **AI-enhanced Evaluation**",
            f"**Summary**: {self.summary}",
            "**Completeness**:",
            f" - Title: {yn_emoji(self.title_complete)}\n",
            f" - Description: {yn_emoji(self.description_complete)}\n",
            f" - Acceptance Criteria: {yn_emoji(self.acceptance_criteria_complete)}\n\n",
            f"**Importance**: {self.importance}\n\n",
            f"**Acceptance Criteria Evaluation**: {self.acceptance_criteria_evaluation}\n\n",
            f"**Suggested Labels**: {', '.join(self.labels)}\n\n",
            f"**Ready to Work**: {yn_emoji(self.ready_to_work)}\n",
        ]
        if not self.ready_to_work and self.base_story_not_clear:
            lines.append(
                "\n**❌ Refactored Story could not be provided because the original story is unclear or lacks meaningful value. Please rewrite the title and description to clearly explain the story's purpose and value.**"
            )
        if self.suggestions and (not self.ready_to_work and not self.base_story_not_clear):
            lines.append("\n### Refactored Story")
            lines.append(self.suggestions.to_markdown())
        return "\n".join(lines)
