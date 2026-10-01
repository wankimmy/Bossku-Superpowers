"""calc.py"""
import re

_TOKEN_RE = re.compile(r"\s*(?:(\d+\.\d+|\d+)|([+\-*/()]))")


def _tokenize(expr):
    tokens = []
    pos = 0
    length = len(expr)
    while pos < length:
        if expr[pos].isspace():
            pos += 1
            continue
        m = _TOKEN_RE.match(expr, pos)
        if not m or m.end() == pos:
            raise ValueError(f"invalid character at position {pos}: {expr[pos]!r}")
        if m.group(1) is not None:
            tokens.append(("NUM", float(m.group(1))))
        else:
            tokens.append(("OP", m.group(2)))
        pos = m.end()
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self):
        value = self.parse_expr()
        if self.peek() is not None:
            raise ValueError(f"unexpected token: {self.peek()}")
        return value

    def parse_expr(self):
        value = self.parse_term()
        while True:
            tok = self.peek()
            if tok == ("OP", "+"):
                self.advance()
                value += self.parse_term()
            elif tok == ("OP", "-"):
                self.advance()
                value -= self.parse_term()
            else:
                break
        return value

    def parse_term(self):
        value = self.parse_factor()
        while True:
            tok = self.peek()
            if tok == ("OP", "*"):
                self.advance()
                value *= self.parse_factor()
            elif tok == ("OP", "/"):
                self.advance()
                divisor = self.parse_factor()
                if divisor == 0:
                    raise ValueError("division by zero")
                value //= divisor
            else:
                break
        return value

    def parse_factor(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        if tok == ("OP", "-"):
            self.advance()
            return -self.parse_factor()
        if tok == ("OP", "("):
            self.advance()
            value = self.parse_expr()
            if self.peek() != ("OP", ")"):
                raise ValueError("unbalanced parentheses")
            self.advance()
            return value
        if tok[0] == "NUM":
            self.advance()
            return tok[1]
        raise ValueError(f"unexpected token: {tok}")


def evaluate(expr):
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("expression must be a non-empty string")
    tokens = _tokenize(expr)
    parser = _Parser(tokens)
    return float(parser.parse())
