from lib.Lexer import Lexer
from lib.TokenType import TokenType

tokenTypesList: list = [
    TokenType('IF', 'if'),
    TokenType('WHILE', 'while'),
    TokenType('NUMBER', '[0-9]+'),
    TokenType('FLOAT', '\d*\.\d+'),
    TokenType('VARIABLE', '[a-zA-Z][a-zA-Z0-9]*'),
    TokenType('SEMICOLON', ';'),
    TokenType('BLOCK_START', '{'),
    TokenType('BLOCK_END', '}'),
    TokenType('ASSIGN', '='),
    TokenType('SPACE', '[ \\n\\t\\r]'),
    TokenType('PLUS', '\+'),
    TokenType('MINUS', '-'),
    TokenType('MULTIPLICATION', '\*'),
    TokenType('DIVISION', '\/'),
    TokenType('OPEN_BRACKET', '\('),
    TokenType('CLOSE_BRACKET', '\)'),
    TokenType('EQUAL', '=='),
    TokenType('LESS', '<'),
    TokenType('GREATER', '>'),
    TokenType('NOT_EQUAL', '!='),
    TokenType('AND', '&&'),
    TokenType('OR', '||'),
]

lexer: Lexer = Lexer(tokenTypesList)

code = ("n1=12;\n"
        "n1= n1 + 2;\n"
        "if(n1 < 13)\n"
        "{ n1 = n1 + 100}\n"
        "ifwhile(if)"
        "{}")

for token in lexer.lex_analysis(code):
    print(str(token))
