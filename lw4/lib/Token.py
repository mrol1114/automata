from .TokenType import TokenType


class Token:
    def __init__(self, type: str, id: str, value: str, pos: int):
        self.type: str = type
        self.id: str = id
        self.pos: int = pos
        self.value: str = value

    def __str__(self):
        return "Object Token: \n\ttype - % s, \n\tid - % s, \n\tpos - % s, \n\tvalue - % s\n" % (self.type, self.id, self.pos, self.value)
