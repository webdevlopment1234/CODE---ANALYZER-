import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL_NAME = 'gemini-3.6-flash'

PROMPT_TEMPLATE = (
    "You are an expert {language} code reviewer.\n"
    "Review the following {language} code and respond in markdown with:\n"
    "1. **Summary** - what the code does in one or two sentences.\n"
    "2. **Bugs & Risks** - potential bugs, edge cases, or security issues.\n"
    "3. **Code Quality** - readability, naming, structure, and style issues.\n"
    "4. **Performance** - any performance concerns.\n"
    "5. **Suggestions** - concrete improvements (with small code snippets if helpful).\n"
    "Be concise and specific. If the code is already good, say so.\n\n"
    "```{language}\n{code}\n```"
)


PLACEHOLDER_KEYS = {'', 'your_api_key_here'}


def _get_api_key():
    for name in ('GOOGLE_API_KEY', 'GEMINI_API_KEY', 'API_KEY'):
        value = os.getenv(name, '').strip()
        if value.lower() not in PLACEHOLDER_KEYS:
            return value
    return None


def get_ai_review(code, language):
    api_key = _get_api_key()
    if not api_key:
        return {
            'success': False,
            'review': (
                'Gemini API key not configured. '
                'Create a `.env` file in the project root containing:\n\n'
                '`GOOGLE_API_KEY=your_api_key_here`'
            ),
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = PROMPT_TEMPLATE.format(language=language, code=code)
        response = model.generate_content(prompt)
        review = response.text
        if not review:
            raise ValueError('Empty response from Gemini.')
        return {'success': True, 'review': review}
    except Exception as e:
        return {'success': False, 'review': f'AI review failed: {e}'}
