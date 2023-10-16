from tokenizer import Token, TokenType


class Parser:
    """
    A class for parsing mathematical expressions into tokens.

    Attributes:
        operators (dict): The operators used in the expression.
    """

    def __init__(self, operators):
        """
        Initialize a Parser object with an expression and a set of operators.

        Args:
            operators (dict): A string containing the allowed operators.
        """
        self.operators = operators

    def parse(self, expression) -> list[Token]:
        """
        Parse a mathematical expression into a postfix notation.

        Args:
            expression (str): The input mathematical expression to be parsed.

        Returns:
            list[TokenType, float | str]: A list of tokens in postfix notation representing the expression.

        Raises:
            ValueError: If there are mismatched parentheses in the expression.

        This method tokenizes the input expression, then converts it into a list
        of tokens in postfix notation using the Shunting Yard algorithm. It handles
        numbers, functions, operators, and parentheses to create a valid postfix
        notation representation of the expression.
        """

        postfix = []  # Output list for the postfix notation
        stack = []  # Stack for operators and parentheses
        tokens = self._tokenize(expression)  # Tokenize the input expression

        for token in tokens:

            if token == TokenType.NUMBER:
                postfix.append(token)

            elif token == TokenType.FUNCTION:
                stack.append(token)

            elif token == TokenType.OPERATOR:
                # Handle operators based on precedence and associativity
                while (stack and stack[-1] == TokenType.OPERATOR
                       and stack[-1].value != '('
                       and self.operators[token.value][0] <= self.operators[stack[-1].value][0]):
                    postfix.append(stack.pop())
                stack.append(token)

            elif token == TokenType.PARENTHESIS:
                if token.value == '(':
                    stack.append(token)
                elif token.value == ')':
                    # Pop operators from the stack until an opening parenthesis is encountered
                    while stack and stack[-1].value != '(':
                        postfix.append(stack.pop())
                    if stack and stack[-1].value == '(':
                        stack.pop()
                    else:
                        raise ValueError("Mismatched parentheses")

        # Pop any remaining operators from the stack to postfix
        while stack:
            if stack[-1] == TokenType.PARENTHESIS:  # Check for unmatched parentheses
                raise ValueError("Mismatched parentheses")
            postfix.append(stack.pop())

        return postfix  # Return the postfix notation of the expression

    def _tokenize(self, expression) -> list[Token]:
        """
        Tokenize the input expression and convert it into a list of tokens.

        Args:
            expression (str): A string containing the allowed operators.

        Returns:
            list[TokenType, float | str]: A list of Token objects representing the expression.

        Raises:
            ValueError: If the given expression is invalid.
        """

        tokens = []
        i = 0

        # Traverse till end of expression
        while i < len(expression):

            # Process numbers
            if expression[i].isdigit() or expression[i] == '.':
                num = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                tokens.append(Token(TokenType.NUMBER, float(num)))

            # Process function names
            elif expression[i].isalpha():
                func_name = ''
                while i < len(expression) and expression[i].isalpha():
                    func_name += expression[i]
                    i += 1
                tokens.append(Token(TokenType.FUNCTION, func_name))

            # Process operators
            elif expression[i] in self.operators:
                tokens.append(Token(TokenType.OPERATOR, expression[i]))
                i += 1

            # Process parentheses
            elif expression[i] == '(' or expression[i] == ')':
                tokens.append(Token(TokenType.PARENTHESIS, expression[i]))
                i += 1

            # Skip spaces
            elif expression[i] == ' ':
                i += 1

            else:
                # Raise an error for invalid characters
                raise ValueError(f"Invalid expression: {expression[i]}")
        return tokens


if __name__ == '__main__':
    # Testing
    exp = '3*(10+5)'
    op = {
        '+': (1, lambda p, q: p + q),
        '-': (1, lambda p, q: p - q),
        '*': (2, lambda p, q: p * q),
        '/': (2, lambda p, q: p / q)
    }
    par = Parser(op)
    postfix_exp = par.parse(exp)
    print(postfix_exp)
