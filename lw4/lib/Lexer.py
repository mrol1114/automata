import re

from .TokenType import TokenType
from .Token import Token


class Lexer:
    def __init__(self, token_type_list: list):
        self.token_type_list : list = token_type_list
        self.id_str : str = 'ID'
        self.pos : int = 0
        self.token_id : int = 0

    def lex_analysis(self, code: str) -> list:
        self.pos = 0
        self.token_id = 0
        tokens: list = []

        while self.next_token(code, tokens):
            continue

        return self.clear_space_tokens(tokens)

    def next_token(self, code: str, tokens: list) -> bool:
        if self.pos >= len(code):
            return False

        token_type: TokenType
        for token_type in self.token_type_list:
            match_obj = re.match(token_type.regex, code[self.pos:])
            if match_obj and match_obj.group():
                tokens.append(
                    Token(token_type.name, self.id_str + str(self.token_id), code[match_obj.start() + self.pos:match_obj.end() + self.pos],
                          match_obj.start()))
                self.token_id += 1
                self.pos += match_obj.end()

                return True

        raise Exception("Error at position " + str(self.pos))

    @staticmethod
    def clear_space_tokens(tokens: list) -> list:
        return list(filter(lambda token: token.type != 'SPACE', tokens))
