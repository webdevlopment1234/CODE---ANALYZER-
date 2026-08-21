import pandas as pd
import streamlit as st
from streamlit_ace import st_ace

from complexity import RANK_DESCRIPTIONS, analyze_complexity
from reviewer import get_ai_review
from static_analysis import analyze_static
from syntax_checker import check_syntax
from utils import LANGUGE_CONFIG, SAMPLE_CODE, get_file_extension, get_language_config

st.set_page_config(page_title='Code Analyzer', page_icon='🔍', layout='wide')

st.title('🔍 Code Analyzer')
st.caption('Syntax checking, static analysis, complexity metrics and AI-powered code review.')


@st.cache_data(show_spinner=False)
def cached_review(code, language):
    return get_ai_review(code, language)


with st.sidebar:
    st.header('⚙️ Settings')
    language = st.selectbox('Language', list(LANGUGE_CONFIG.keys()), index=0).lower()
    config = get_language_config(language)

    allowed_exts = [cfg['ext'].lstrip('.') for cfg in LANGUGE_CONFIG.values()]
    uploaded = st.file_uploader('Upload a file (optional)', type=allowed_exts)
    analyze_btn = st.button('🚀 Analyze Code', type='primary', use_container_width=True)

if uploaded is not None:
    code = uploaded.getvalue().decode('utf-8', errors='replace')
else:
    code = st_ace(
        value=SAMPLE_CODE.get(language, ''),
        language=config['ace_mode'],
        theme='monokai',
        font_size=14,
        height=380,
        wrap=True,
        key=f'editor_{language}',
    )


def render_issues(syntax_result, bugs):
    syntax_errors = [] if syntax_result['Valid'] else syntax_result['bugs']
    total_issues = len(syntax_errors) + len(bugs)

    if not syntax_errors and not bugs:
        st.success('✅ No issues found. The code passed syntax and static analysis.')
        return

    if syntax_errors:
        with st.expander(f'❌ Syntax Errors ({len(syntax_errors)})', expanded=True):
            st.dataframe(pd.DataFrame(syntax_errors), use_container_width=True, hide_index=True)

    if bugs:
        with st.expander(f'🐛 Static Analysis Issues ({len(bugs)})', expanded=True):
            st.dataframe(pd.DataFrame(bugs), use_container_width=True, hide_index=True)


def render_complexity(results, avg):
    if avg is None:
        st.info(f'Complexity analysis is only available for Python (radon does not parse {language.title()}).')
        return

    if not results:
        st.info('No functions or classes detected to measure complexity.')
        return

    col1, col2 = st.columns(2)
    col1.metric('Average Cyclomatic Complexity', avg)
    worst = max(results, key=lambda r: r['complexity'])
    col2.metric('Most Complex Block', f"{worst['name']} ({worst['complexity']})")

    df = pd.DataFrame(results)
    df['risk'] = df['rank'].map(RANK_DESCRIPTIONS)
    st.dataframe(df, use_container_width=True, hide_index=True)

    risky = [r for r in results if r['rank'] not in ('A', 'B')]
    if risky:
        st.warning(f"⚠️ {len(risky)} block(s) have a cyclomatic complexity above 5 — consider refactoring.")


if analyze_btn:
    if not code.strip():
        st.warning('Please enter or upload some code to analyze.')
        st.stop()

    syntax_result = check_syntax(code, language)
    bugs = analyze_static(code, language)
    complexity_results, avg_complexity = analyze_complexity(code, language)

    st.subheader('📋 Results')

    m1, m2, m3, m4 = st.columns(4)
    m1.metric('Syntax', 'Valid ✅' if syntax_result['Valid'] else 'Invalid ❌')
    issue_count = len(bugs) + (0 if syntax_result['Valid'] else len(syntax_result['bugs']))
    m2.metric('Issues Found', issue_count)
    m3.metric('Blocks Measured', len(complexity_results) if avg_complexity is not None else 'N/A')
    m4.metric('Avg Complexity', avg_complexity if avg_complexity is not None else 'N/A')

    issues_tab, complexity_tab, ai_tab = st.tabs(['🐞 Issues', '📈 Complexity', '🤖 AI Review'])

    with issues_tab:
        render_issues(syntax_result, bugs)

    with complexity_tab:
        render_complexity(complexity_results, avg_complexity)

    with ai_tab:
        with st.spinner('Getting AI review from Gemini...'):
            review = cached_review(code, language)
        if review['success']:
            st.markdown(review['review'])
        else:
            st.error(review['review'])
else:
    st.info('⬅️ Paste or upload your code in the editor, then click **Analyze Code**.')
