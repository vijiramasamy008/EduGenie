# EduGenie – Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the uploaded project
documentation. It provides:

- Question & Answer
- Simple concept explanation
- MCQ quiz generation
- Passage summarization
- Personalized learning paths

## Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## 1. Install Python

Use Python 3.10 or newer.

Check:

```bash
python --version
```

On Windows, if `python` does not work, try:

```bash
py --version
```

## 2. Open the project in VS Code

Open the `EduGenie` folder in VS Code.

Then open:

**Terminal → New Terminal**

## 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The requirements include the optional local LaMini-Flan-T5 dependencies because
the original documentation specifies LaMini-Flan-T5 for concept explanation.

For the easiest setup, keep:

```text
ENABLE_LOCAL_EXPLAINER=false
```

The application will then use Gemini for explanations too. If you later want
the local model, change it to `true`.

## 5. Add your Gemini API key

Copy:

```text
.env.example
```

to:

```text
.env
```

Then open `.env` and replace:

```text
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

with your actual key.

Never commit `.env` to GitHub.

The current default model in this project is configurable through:

```text
GEMINI_MODEL=gemini-2.5-flash
```

If your Google AI account exposes a different Gemini model, change that value.

## 6. Run EduGenie

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 7. Test the API

Health check:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

From `/docs`, you can test:

- POST `/qa`
- POST `/explain`
- POST `/quiz`
- POST `/summarize`
- POST `/learn/recommendations`

## 8. Functional test checklist

### Q&A
Enter:

```text
What is photosynthesis?
```

Choose **Ask a Question** and click Generate.

### Explanation
Enter:

```text
Explain the Pythagoras theorem
```

Choose **Explain a Topic**.

### Quiz
Paste a paragraph about any academic topic and choose **Generate Quiz**.
The default is three questions with four options each.

### Summary
Paste a long study paragraph and choose **Summarize**.

### Learning path
Enter:

```text
Python programming
```

Choose **Learning Path** and select a level.

## Troubleshooting

### `GEMINI_API_KEY is missing`

Make sure `.env` exists in the same folder as `main.py` and contains:

```text
GEMINI_API_KEY=your_key_here
```

Restart Uvicorn after changing `.env`.

### PowerShell does not allow activation

You can either use Command Prompt:

```cmd
.venv\Scripts\activate
```

or configure PowerShell execution policy according to your organization's
security rules. You can also run the virtual environment's Python directly.

### Local LaMini model is slow or fails

Set:

```text
ENABLE_LOCAL_EXPLAINER=false
```

EduGenie will use Gemini for explanations. The local model is intentionally
optional because it can require substantial RAM, disk space and download time.

### Gemini model error

Change `GEMINI_MODEL` in `.env` to a Gemini model available to your API key.

## Notes about the supplied project document

The supplied document names Gemini 1.5 Pro and LaMini-Flan-T5-783M. Gemini model
availability changes over time, so the code keeps the model name configurable
through `.env` instead of hard-coding a historical model name. The application
still implements the same five user-facing modules and FastAPI endpoints
described in the document.
