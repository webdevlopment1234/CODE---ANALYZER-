from radon.complexity import average_complexity, cc_rank, cc_visit

from utils import get_language_config

RANK_DESCRIPTIONS = {
    'A': 'Low risk - well structured block',
    'B': 'Moderate risk - slightly complex',
    'C': 'High risk - complex, hard to maintain',
    'D': 'Very high risk - needs refactoring',
    'E': 'Dangerous - strongly consider refactoring',
    'F': 'Error prone - must be refactored immediately',
}


def analyze_complexity(code, language):
    config = get_language_config(language)
    if not config or not config.get('supports_radon'):
        return [], None

    try:
        blocks = cc_visit(code)
    except Exception:
        return [], None

    results = []
    for block in blocks:
        results.append({
            'name': block.name,
            'type': type(block).__name__,
            'line': block.lineno,
            'complexity': block.complexity,
            'rank': cc_rank(block.complexity),
        })

    avg = round(average_complexity(blocks), 2) if blocks else 0
    return results, avg
