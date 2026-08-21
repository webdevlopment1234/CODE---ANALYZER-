import ast
def check_syntax(code,language):
    if language != 'python':
        return{
            'Valid': True,
            'bugs': []
        }
    try:
        ast.parse(code)
        return {
            'Valid': True,
            'bugs': []
        }
    except SyntaxError as e:
        return {
            'Valid': False,
            'bugs': [{
                'line': e.lineno,
                'offset': e.offset,
                'description':f" Syntax Error: {e.msg}"
            }]
        }