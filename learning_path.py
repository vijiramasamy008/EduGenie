from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = f"""
Create a personalized learning path for:

Topic: {topic}
Learner level: {level}

Organize it from the learner's current level toward advanced understanding.

Include:
- Stage/topic
- What to learn
- Suggested practice
- A realistic time estimate
- Recommended resource types (videos, documentation, books, practice sites)

Keep the plan practical and beginner-friendly. Do not fabricate specific
links or claim that a resource was checked.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, a personalized learning-path mentor.",
    )
