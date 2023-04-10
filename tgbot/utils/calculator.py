# -----------------------------------------------------------------------------
# calc.py
# import sys
#
# sys.path.insert(0, '../..')
# -----------------------------------------------------------------------------
import decimal
from typing import Optional

from sly import Lexer, Parser

from tgbot.utils.decimals import format_decimal


def calc_expression(expression: str) -> Optional[str]:
    parser_ = CalcParser()
    lexer_ = CalcLexer()
    return format_decimal(parser_.parse(lexer_.tokenize(expression)), pre=4)


class CalcLexer(Lexer):
    tokens = {NAME, INTEGER, DECIMAL, PLUS, TIMES, MINUS, DIVIDE, PERCENT, LPAREN, RPAREN}
    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    DECIMAL = r'(\d*\.\d+)|(\d+\.\d*)'
    INTEGER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    PERCENT = r'%'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    # def ignore_newline(self, t):
    #     self.lineno += t.value.count('\n')

    def error(self, t):
        self.index += 1
        if t:
            raise RuntimeError(f"Syntax error at '{t.value[0]}'")
        else:
            raise RuntimeError(f"Syntax error at EOF")


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('left', PERCENT),
        ('right', UMINUS)
    )

    def __init__(self, builtins=None):
        self.names = {}
        self.builtins = builtins

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr PLUS expr PERCENT')
    def expr(self, p):
        return p.expr0 + p.expr0 * p.expr1 / 100

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr MINUS expr PERCENT')
    def expr(self, p):
        return p.expr0 - p.expr0 * p.expr1 / 100

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr TIMES expr PERCENT')
    def expr(self, p):
        return p.expr0 * p.expr1 / 100

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('expr DIVIDE expr PERCENT')
    def expr(self, p):
        return 100 * p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('INTEGER')
    def expr(self, p):
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        return decimal.Decimal(p.INTEGER)

    @_('DECIMAL')
    def expr(self, p):
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        return decimal.Decimal(p.DECIMAL)

    def error(self, token):
        """
        Default error handling function.  This may be subclassed.
        """
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                raise RuntimeError(f"Parser: Syntax error at line {lineno}, token={token.type}\n")
            else:
                raise RuntimeError(f"Parser: Syntax error, token={token.type}")
        else:
            raise RuntimeError(f"Parser: Parse error in input. EOF\n")


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            # parser.parse(lexer.tokenize(text))
            print(format_decimal(parser.parse(lexer.tokenize(text))))
