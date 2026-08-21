import json
import re

LANGUGE_CONFIG = {
    'python': {
        'ace_mode': 'python',
        'ext': '.py',
        'supports_radon': True
    },
    'c++': {
        'ace_mode': 'c_cpp',
        'ext': '.cpp',
        'supports_radon': False
    },
    'java': {
        'ace_mode': 'java',
        'ext': '.java',
        'supports_radon': False
    }
}


def get_language_config(language):
    if not language:
        return None
    language = language.lower()
    return LANGUGE_CONFIG.get(language)


def get_file_extension(language):
    config = get_language_config(language)
    return config['ext'] if config else '.txt'


SAMPLE_CODE = {
    'python': (
        'def calculate_area(radius):\n'
        '    PI = 3.14159\n'
        '    return PI * radius ** 2\n'
        '\n'
        'def greet(name, greeting="Hello"):\n'
        '    return f"{greeting}, {name}!"\n'
        '\n'
        'print(greet("World"))\n'
    ),
    'c++': (
        '#include <iostream>\n'
        '\n'
        'int main() {\n'
        '    std::cout << "Hello, World!" << std::endl;\n'
        '    return 0;\n'
        '}\n'
    ),
    'java': (
        'public class Main {\n'
        '    public static void main(String[] args) {\n'
        '        System.out.println("Hello, World!");\n'
        '    }\n'
        '}\n'
    ),
}
