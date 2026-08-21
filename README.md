# Code Analyzer

A web-based code analysis tool built with Streamlit. Paste or upload your code to get instant syntax checking, static analysis, cyclomatic complexity metrics, and an AI-powered code review from Google Gemini.

## Features

- **Syntax Checking** - Detects Python syntax errors with exact line and column positions.
- **Static Analysis** - Finds bugs like function calls with too few or too many arguments by parsing the AST.
- **Complexity Metrics** - Measures cyclomatic complexity of functions and classes using [radon](https://radon.readthedocs.io/), highlights blocks above a complexity of 5 for refactoring.
- **AI Code Review** - Sends your code to Google Gemini and returns a structured markdown review covering summary, bugs and risks, code quality, performance, and concrete suggestions.
- **Multi-language Editor** - Built-in Ace editor with syntax highlighting, plus optional file upload.

## Supported Languages

| Language | Syntax Check | Static Analysis | Complexity | AI Review |
|----------|:------------:|:---------------:|:----------:|:---------:|
| Python   | Yes | Yes | Yes | Yes |
| C++      | -   | -   | -   | Yes |
| Java     | -   | -   | -   | Yes |

Deep analysis currently runs on Python source only; other languages get the AI-powered review.

## Getting Started

### Prerequisites

- Python 3.10+
- A free Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/webdevlopment1234/CODE---ANALYZER-.git
   cd CODE---ANALYZER-
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # Linux / macOS
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:

   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

   The key is also read from `GEMINI_API_KEY` or `API_KEY` if you prefer those names.

### Running the App

```bash
streamlit run app.py
```

Then open the URL shown in your terminal (usually `http://localhost:8501`). Choose a language in the sidebar, paste or upload your code, and click **Analyze Code**.

## Project Structure

```
code-Analyzer/
├── app.py               # Streamlit UI and result rendering
├── reviewer.py          # Gemini-powered AI code review
├── syntax_checker.py    # Python syntax validation (ast.parse)
├── static_analysis.py   # AST-based argument-mismatch detection
├── complexity.py        # Cyclomatic complexity via radon
├── utils.py             # Language config and sample code
├── requirements.txt
└── .env                 # API keys (not committed)
```

## Tech Stack

- [Streamlit](https://streamlit.io/) - Web framework
- [streamlit-ace](https://github.com/okld/streamlit-ace) - In-browser code editor
- [google-generativeai](https://pypi.org/project/google-generativeai/) - Gemini API client
- [radon](https://radon.readthedocs.io/) - Cyclomatic complexity analysis
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable loading

## Security Notes

- Never commit your `.env` file. It is already listed in `.gitignore`.
- If an API key is accidentally exposed, revoke and regenerate it in [Google AI Studio](https://aistudio.google.com/apikey).
