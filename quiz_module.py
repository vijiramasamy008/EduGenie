import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _validate_quiz(data: Any, num_questions: int) -> list[dict[str, Any]]:
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON array.")

    validated = []
    for index, item in enumerate(data[:num_questions], start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is not an object.")

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        answer = str(item.get("answer", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must contain exactly four options.")

        options = [str(option).strip() for option in options]
        if any(not option for option in options):
            raise ValueError(f"Question {index} has an empty option.")

        if answer not in options:
            raise ValueError(
                f"Question {index} answer must exactly match one of its options."
            )

        validated.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": str(item.get("explanation", "")).strip(),
            }
        )

    if len(validated) != num_questions:
        raise ValueError("Gemini did not return the requested number of questions.")

    return validated


def generate_quiz(text: str, num_questions: int = 3) -> list[dict[str, Any]]:
    prompt = f"""
Generate exactly {num_questions} multiple-choice questions from the passage below.

PASSAGE:
{text}

Return ONLY valid JSON. No Markdown and no code fences.

Required JSON shape:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Exactly one option string",
    "explanation": "Short explanation of why the answer is correct"
  }}
]

Rules:
- Exactly four options per question.
- Exactly one correct answer.
- Questions must be answerable from the passage.
- Distractors should be plausible.
"""
    raw = generate_text(
        prompt,
        system_instruction="You generate reliable educational MCQs in strict JSON.",
        temperature=0.2,
    )

    cleaned = clean_json_block(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse Gemini quiz JSON: {exc}") from exc

    return _validate_quiz(data, num_questions)
