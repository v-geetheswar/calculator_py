import math
from parser import *


class Evaluator:

    def __init__(self, is_deg: bool = False):
        """
        Initializes the Evaluator.

        Args:
            is_deg (bool): Indicates whether trigonometric functions should expect degrees instead of radians.
        """
        self.is_deg: bool = is_deg

        self.is_trig: list[str] = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']

        self.functions: dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'log': math.log10,
            'ln': math.log,
            'abs': abs
        }

        self.operators: dict = {
            '+': (1, lambda x, y: x + y),
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y),
            '/': (2, lambda x, y: x / y),
            '^': (3, lambda x, y: x ** y),
            '!': (4, math.factorial)
        }

    def evaluate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression in postfix notation and returns the result.

        Args:
            expression (str): The mathematical expression in postfix notation.

        Returns:
            float: The result of the expression evaluation.
        """
        parser = Parser(self.operators)
        postfix = parser.parse(expression)
        return self._postfix_eval(postfix)

    def _postfix_eval(self, postfix: list[Token]) -> float:
        """
        Evaluates a mathematical expression in postfix notation.

        Args:
            postfix (list[Token]): The mathematical expression in postfix notation.

        Returns:
            float: The result of the expression evaluation.
        """
        stack = []
        for token in postfix:
            if token == TokenType.NUMBER:
                stack.append(token.value)

            elif token == TokenType.FUNCTION:
                if token.value in self.functions:
                    arg = stack.pop()
                    if token.value in self.is_trig and self.is_deg:
                        arg = math.radians(arg)
                    result = self.functions[token.value](arg)
                    stack.append(result)
                else:
                    raise ValueError(f"Unknown function: {token.value}")

            elif token == TokenType.OPERATOR:
                if token.value == '!':
                    if len(stack) < 1:
                        raise ValueError("Insufficient operands for factorial")
                    operand = int(stack.pop())
                    result = self.operators[token.value][1](operand)
                    stack.append(result)
                else:
                    if len(stack) < 2:
                        raise ValueError("Insufficient operands for operator")
                    right_operand = stack.pop()
                    left_operand = stack.pop()
                    result = self.operators[token.value][1](left_operand, right_operand)
                    stack.append(result)

        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]


if __name__ == '__main__':
    e = Evaluator(True)
    print(e.evaluate('1+2+3+4+sin(90)'))
