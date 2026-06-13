from resume_q_a.app import build_assistant, describe_project, generate_response


def test_description_mentions_subject():
    assert 'Resume Q&A' in describe_project()


def test_generate_response_uses_real_agent_output():
    response = generate_response("help me plan a useful workflow")

    assert 'Resume Q&A' in response
    assert "Sources:" in response
    assert "Next actions:" in response


def test_build_assistant_for_project_type():
    assistant = build_assistant()

    assert assistant.project_type == 'RAG'
    assert assistant.subject == 'Resume Q&A'

