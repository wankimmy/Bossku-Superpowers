"""A tiny, safe arithmetic-expression evaluator for stat formulas.

Formulas come from other people's exported stat sheets, so they are
untrusted input -- never hand them to eval()/exec() or anything else
that can run arbitrary code. This walks the parsed AST itself and only
allows +, -, *, /, parentheses, numbers, and names resolved through the
caller-supplied `resolve` callback.
"""

import ast
import operator

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class FormulaError(Exception):
    """Raised when a formula string can't be parsed or evaluated safely."""


def evaluate_formula(expression, resolve):
    """Evaluate a simple +-*/() arithmetic expression.

    `resolve` is called with a cell name whenever the expression
    references one, and should return that cell's current value (or
    raise) -- names are looked up lazily, one at a time, rather than by
    building a dict of every known cell up front.
    """
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise FormulaError(f"invalid formula: {expression!r}") from exc
    return _eval_node(parsed.body, resolve)


def _eval_node(node, resolve):
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        left = _eval_node(node.left, resolve)
        right = _eval_node(node.right, resolve)
        return _BIN_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand, resolve))
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        return resolve(node.id)
    raise FormulaError(f"unsupported expression: {ast.dump(node)}")
