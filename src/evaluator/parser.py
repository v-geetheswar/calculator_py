from tokenizer import Token, TokenType


class Parser:
    """
    A class for parsing mathematical expressions into tokens.

    Attributes:
        expression (str): The input mathematical expression.
        operators (dict): The operators used in the expression.
    """

    def __init__(self, expression, operators):
        """
        Initialize a Parser object with an expression and a set of operators.

        Args:
            expression (str): The mathematical expression to parse.
            operators (dict): A string containing the allowed operators.
        """
        self.expression = expression
        self.operators = operators

    def tokenize(self):
        """
        Tokenize the input expression and convert it into a list of tokens.

        Returns:
            list: A list of Token objects representing the expression.
        """

        expr = self.expression
        tokens = []
        i = 0

        # Traverse till end of Expression
        while i < len(expr):

            # Process numbers
            if expr[i].isdigit() or expr[i] == '.':
                num = ''
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                tokens.append(Token(TokenType.NUMBER, float(num)))

            # Process function names
            elif expr[i].isalpha():
                func_name = ''
                while i < len(expr) and expr[i].isalpha():
                    func_name += expr[i]
                    i += 1
                tokens.append(Token(TokenType.FUNCTION, func_name))

            # Process operators
            elif expr[i] in self.operators:
                tokens.append(Token(TokenType.OPERATOR, expr[i]))
                i += 1

            # Process parentheses
            elif expr[i] == '(' or expr[i] == ')':
                tokens.append(Token(TokenType.PARENTHESIS, expr[i]))
                i += 1

            # Skip spaces
            elif expr[i] == ' ':
                i += 1

            else:
                # Raise an error for invalid characters
                raise ValueError(f"Invalid expr: {expr[i]}")
        return tokens


if __name__ == '__main__':
    # Testing
    exp = '1+2-3*4/10+sin(0)'
    op = {
        '+': (1, lambda x, y: x + y),
        '-': (1, lambda x, y: x - y),
        '*': (2, lambda x, y: x * y),
        '/': (2, lambda x, y: x / y)
    }
    parser = Parser(exp, op)
    tks = parser.tokenize()
    print(tks)
