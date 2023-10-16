from enum import Enum


# Define an enumeration to represent different token types.
class TokenType(Enum):
    NUMBER = 0
    OPERATOR = 1
    FUNCTION = 2
    PARENTHESIS = 3


class Token:
    """
    Represents a token in a mathematical expression.

    Args:
        token_type (TokenType): The type of the token, which can be NUMBER, OPERATOR, FUNCTION, or PARENTHESIS.
        value (float | str): The value of the token, which is the actual symbol or text representing the token.
    """

    def __init__(self, token_type: TokenType, value: float | str):
        """
        Initialize a Token object with a token_type and the value assigned to it.

        Args:
            token_type (TokenType): The type of the token, which can be NUMBER, OPERATOR, FUNCTION, or PARENTHESIS.
            value (float | str): The value of the token, which is the actual symbol or text representing the token.
        """
        self.token_type = token_type
        self.value = value

    def __eq__(self, other):
        """
        Compare the type of this token with another token or TokenType.

        Args:
            other: The token or TokenType to compare with.

        Returns:
            bool: True if the types match, False otherwise.
        """

        if isinstance(other, Token):
            return self.token_type == other.token_type
        if isinstance(other, TokenType):
            return self.token_type == other
        return self.token_type.value == other

    def __repr__(self):
        # for development purpose
        # used to print the return string on print call
        # rather than memory location
        return f'{self.token_type.name, self.value}'


if __name__ == '__main__':
    # Testing of Token and TokenType
    a = Token(TokenType.NUMBER, 0)
    b = Token(TokenType.NUMBER, 5)
    if a == TokenType.NUMBER:
        print(True)
    if a == b:
        print(True)
    # 1 -> OPERATOR
    if a != 1:
        print(False)
