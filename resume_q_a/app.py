from .agents import BaseAgent, agent_for_type
from .config import CONFIG
from .knowledge import load_documents


PROJECT_TYPE = CONFIG.project_type
PROJECT_SUBJECT = CONFIG.project_subject


def describe_project() -> str:
    return (
        f"{PROJECT_SUBJECT} is a production-shaped {PROJECT_TYPE} starter with "
        "local data, agent logic, a CLI, and tests."
    )


def build_assistant() -> BaseAgent:
    documents = load_documents(CONFIG.knowledge_file)
    return agent_for_type(PROJECT_TYPE, PROJECT_SUBJECT, documents)


def generate_response(user_input: str) -> str:
    cleaned = user_input.strip() or "Help me get started"
    return build_assistant().answer(cleaned).as_text()
