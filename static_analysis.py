import ast


class StaticAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.functions = {}
        self.bugs = []

    def visit_FunctionDef(self, node):
        total = len(node.args.args)
        defaults = len(node.args.defaults)
        self.functions[node.name] = {
            'required': total - defaults,
            'max': None if node.args.vararg else total,
        }
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.functions:
            func_name = node.func.id
            signature = self.functions[func_name]
            actual_args = len(node.args) + len(node.keywords)
            if actual_args < signature['required'] or (
                signature['max'] is not None and actual_args > signature['max']
            ):
                expected = signature['required'] if signature['max'] is None \
                    else f"{signature['required']}-{signature['max']}"
                self.bugs.append({
                    'line': node.lineno,
                    'offset': node.col_offset,
                    'description': f"Function '{func_name}' expects {expected} arguments but got {actual_args}."
                })
        self.generic_visit(node)


def analyze_static(code, language):
    if language != 'python':
        return []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    analyzer = StaticAnalyzer()
    analyzer.visit(tree)
    return analyzer.bugs
