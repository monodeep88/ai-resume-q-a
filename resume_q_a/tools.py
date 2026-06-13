import ast
import csv
import operator
from io import StringIO


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> float:
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic is supported")

    return float(evaluate(ast.parse(expression, mode="eval")))


def make_checklist(goal: str) -> list[str]:
    cleaned = goal.strip() or "the user's request"
    return [
        f"Clarify the success criteria for {cleaned}",
        "Gather the smallest useful input sample",
        "Run the assistant and inspect the answer",
        "Add one regression test for the expected behavior",
    ]


def summarize_csv(csv_text: str) -> dict[str, object]:
    rows = list(csv.DictReader(StringIO(csv_text.strip())))
    if not rows:
        return {"rows": 0, "columns": []}
    return {"rows": len(rows), "columns": list(rows[0].keys())}
