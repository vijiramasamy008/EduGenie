from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
Answer the student's question clearly and accurately.

Question:
{question}

Requirements:
- Give the direct answer first.
- Explain the important idea in simple language.
- Use short headings or bullet points when useful.
- If the question is ambiguous, state the assumption you made.
- Do not invent sources, facts, citations, or statistics.
"""
    return generate_text(
        prompt,
        system_instruction=(
            "You are EduGenie, a friendly educational assistant. "
            "Teach rather than merely giving unexplained answers."
        ),
    )
