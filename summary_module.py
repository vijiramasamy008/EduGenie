from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for a student.

Passage:
{text}

Return:
1. A short easy-to-read summary.
2. 3-7 key points.

Keep the important meaning and remove repetition. Do not add information
that is not supported by the passage.
"""
    return generate_text(
        prompt,
        system_instruction="You are an educational summarization assistant.",
    )
