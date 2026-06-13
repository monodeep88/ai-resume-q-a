from dataclasses import dataclass

from .knowledge import Document, search_documents
from .tools import calculate, make_checklist, summarize_csv


@dataclass(frozen=True)
class AgentResponse:
    answer: str
    sources: list[str]
    next_actions: list[str]

    def as_text(self) -> str:
        sources = ", ".join(self.sources) if self.sources else "No sources"
        actions = "\n".join(f"- {action}" for action in self.next_actions)
        return f"{self.answer}\n\nSources: {sources}\n\nNext actions:\n{actions}"


class BaseAgent:
    def __init__(self, subject: str, project_type: str, documents: list[Document]) -> None:
        self.subject = subject
        self.project_type = project_type
        self.documents = documents

    def answer(self, user_input: str) -> AgentResponse:
        raise NotImplementedError


class RAGAgent(BaseAgent):
    def answer(self, user_input: str) -> AgentResponse:
        matches = search_documents(user_input, self.documents)
        summary = " ".join(document.body for document in matches[:2])
        return AgentResponse(
            answer=f"{self.subject} found relevant context and produced this answer: {summary}",
            sources=[document.title for document in matches],
            next_actions=["Review the cited context", "Add domain documents to data/knowledge_base.json"],
        )


class PlannerAgent(BaseAgent):
    def answer(self, user_input: str) -> AgentResponse:
        checklist = make_checklist(user_input)
        return AgentResponse(
            answer=f"{self.subject} converted the request into an execution plan.",
            sources=["Generated planning policy"],
            next_actions=checklist,
        )


class AgenticRAGAgent(BaseAgent):
    def answer(self, user_input: str) -> AgentResponse:
        matches = search_documents(user_input, self.documents)
        checklist = make_checklist(user_input)
        return AgentResponse(
            answer=(
                f"{self.subject} combined retrieval with planning. "
                f"Best context: {matches[0].body}"
            ),
            sources=[document.title for document in matches],
            next_actions=checklist,
        )


class MultiAgentSystem(BaseAgent):
    roles = ("Researcher", "Planner", "Reviewer")

    def answer(self, user_input: str) -> AgentResponse:
        matches = search_documents(user_input, self.documents)
        actions = [
            f"{role}: {step}"
            for role, step in zip(
                self.roles,
                [
                    f"collect evidence from {matches[0].title}",
                    "break the goal into testable milestones",
                    "check that the final answer cites sources",
                ],
            )
        ]
        return AgentResponse(
            answer=f"{self.subject} coordinated {', '.join(self.roles)} agents for the request.",
            sources=[document.title for document in matches],
            next_actions=actions,
        )


class ToolAgent(BaseAgent):
    def answer(self, user_input: str) -> AgentResponse:
        lowered = user_input.lower()
        if "calculate:" in lowered:
            expression = user_input.split(":", 1)[1].strip()
            result = calculate(expression)
            answer = f"{self.subject} calculated {expression} = {result:g}."
            actions = ["Validate the expression", "Use the result in the downstream workflow"]
        elif "csv:" in lowered:
            summary = summarize_csv(user_input.split(":", 1)[1])
            answer = f"{self.subject} inspected a CSV with {summary['rows']} rows and columns {summary['columns']}."
            actions = ["Check missing values", "Add business rules for each column"]
        else:
            answer = f"{self.subject} selected the checklist tool for this request."
            actions = make_checklist(user_input)
        return AgentResponse(answer=answer, sources=["Local tool execution"], next_actions=actions)


def agent_for_type(project_type: str, subject: str, documents: list[Document]) -> BaseAgent:
    if project_type == "RAG":
        return RAGAgent(subject, project_type, documents)
    if project_type == "Agentic AI":
        return PlannerAgent(subject, project_type, documents)
    if project_type == "Agentic RAG":
        return AgenticRAGAgent(subject, project_type, documents)
    if project_type == "Multi-Agent":
        return MultiAgentSystem(subject, project_type, documents)
    if project_type == "Tool Agent":
        return ToolAgent(subject, project_type, documents)
    return RAGAgent(subject, project_type, documents)
