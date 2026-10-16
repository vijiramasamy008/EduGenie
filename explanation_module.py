import os
from functools import lru_cache

from gemini_client import generate_text


@lru_cache(maxsize=1)
def _load_local_model():
    """
    Optional local LaMini-Flan-T5 explanation model.

    Enable with ENABLE_LOCAL_EXPLAINER=true.
    The first use downloads the model from Hugging Face and may require
    significant disk space/RAM. If it cannot be loaded, EduGenie falls
    back to Gemini automatically.
    """
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    model_name = os.getenv(
        "LOCAL_EXPLAINER_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M",
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model


def _local_explain(topic: str) -> str:
    import torch

    tokenizer, model = _load_local_model()
    prompt = (
        "Explain this topic to a beginner using simple language, short examples "
        "and important points: " + topic
    )
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=220,
            num_beams=4,
            early_stopping=True,
        )
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()


def explain_topic(topic: str) -> str:
    use_local = os.getenv("ENABLE_LOCAL_EXPLAINER", "false").lower() == "true"

    if use_local:
        try:
            return _local_explain(topic)
        except Exception:
            # Keep the application usable even if the optional local model
            # cannot be downloaded/loaded on the user's machine.
            pass

    prompt = f"""
Explain the following topic to a beginner.

Topic:
{topic}

Use:
- A simple definition
- 3-6 important points
- One easy example or analogy when appropriate
- Simple language
- A short recap at the end

Avoid unnecessary jargon.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie's concept-explanation tutor.",
    )
