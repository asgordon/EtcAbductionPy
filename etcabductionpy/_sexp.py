'''sexp.py
An S-expression parser in Python
Andrew S Gordon
July 2022'''

class Sexp:
    # a list, a symbol, a number, or a string
    __slots__ = ('type', 'value')
    def __init__(self, type, value):
        if type == 'list' and not isinstance(value, list):
            raise TypeError("Sexp of type list must be a python list")
        if type == 'symbol' and not isinstance(value, str):
            raise TypeError("Sexp of type symbol must be a python string")
        if type == 'number' and not isinstance(value, float):
            raise TypeError("Sexp of type number must be a python float")
        if type == 'string' and not isinstance(value, str):
            raise TypeError("Sexp of type string must be a python string")
        if type not in ['list', 'symbol', 'number', 'string']:
            raise ValueError("Sexp type must be 'list', 'symbol', 'number', or'string'")
        self.type = type
        self.value = value
    def __str__(self):
        if self.type=='symbol': return self.value
        elif self.type=='number': return str(self.value)
        elif self.type=='string': return "\"{}\"".format(self.value)
        elif self.type=='list': return "({})".format(" ".join([str(x) for x in self.value]))
    def to_list(self):
        if self.type=='symbol': return self.value
        elif self.type=='number': return self.value
        elif self.type=='string': return "\"{}\"".format(self.value)
        elif self.type=='list': return [x.to_list() for x in self.value]

class Parser:
    __slots__ = ('input', 'pos', 'depth')
    def __init__(self, src):
        self.input = src
        self.pos = 0
        self.depth = 0

    def parse_first(self):
        self.consume_whitespace_and_comments()
        if self.eof(): raise ValueError("Unexpected end in input line " + str(self.lineno()))
        else:
            return self.parse_sexp()

    def parse_all(self):
        return Sexp('list', self.parse_sexps())

    def parse_sexps(self):
        sexps = []
        while True:
            self.consume_whitespace_and_comments()
            if self.eof() or self.starts_with(')'):
                break
            sexps.append(self.parse_sexp())
        if self.eof() & self.depth > 0: raise ValueError("Unexpected end in input line " + str(self.lineno()))
        if self.starts_with(')') and self.depth == 0: raise ValueError("Unexpeceted close parenthesis in input line " + str(self.lineno()))
        return sexps

    def parse_sexp(self):
        ch = self.next_char()
        if ch in "0123456789-":
            return self.parse_number()
        elif ch == '(':
            return self.parse_list()
        elif ch == '"':
            return self.parse_string()
        else:
            return self.parse_symbol()

    def parse_symbol(self):
        symbol = self.consume_while(lambda x: x not in " ;())\n\t")
        return Sexp('symbol', symbol)

    def parse_number(self):
        number = self.consume_while(lambda x: x not in " ;())\n\t")
        try:
            value = float(number)
        except ValueError:
            raise ValueError("Malformed number \"{}\" in input line {}".format(number, str(self.lineno())))
        return Sexp('number', value)

    def parse_string(self):
        self.consume_char() # opening "
        span = self.consume_while(lambda x: x not in "\"")
        self.consume_char() # closing "
        return Sexp('string',  span )

    def parse_list(self):
        assert(self.consume_char() == '(')
        self.depth += 1
        elements = self.parse_sexps()
        assert(self.consume_char() == ')')
        self.depth -= 1
        return Sexp('list', elements)

    def consume_whitespace_and_comments(self):
        self.consume_whitespace()
        if self.starts_with(';'):
            self.consume_comment()
            self.consume_whitespace_and_comments()
    
    def consume_comment(self):
        self.consume_while(lambda x: x != '\n')

    def consume_whitespace(self):
        self.consume_while(lambda x: x.isspace())

    def consume_while(self, test):
        result = ""
        while not self.eof() and test(self.next_char()):
            result += self.consume_char()
        return result

    def consume_char(self):
        ch = self.input[self.pos]
        self.pos += 1
        return ch

    def starts_with(self, s):
        return self.input[self.pos : self.pos + len(s)] == s

    def next_char(self):
        return self.input[self.pos]

    def eof(self):
        return self.pos >= len(self.input)

    def lineno(self):
        r = 1
        for c in self.input:
            if c == '\n': r += 1
        return r


if __name__ == "__main__": # run tests
    
    assert str(Parser(" one ").parse_first()) == "one"

    assert str(Parser("  :symbol seven").parse_first()) == ":symbol"

    assert str(Parser("0002002039932.939292").parse_first()) == "2002039932.939292" # fails in python2

    assert str(Parser("( predicate arg1   \n :keyword1 \"string\" \t -0.9399)").parse_first()) == "(predicate arg1 :keyword1 \"string\" -0.9399)"

    assert str(Parser("one\n two\n :three\n -04.0").parse_sexps()[3]) == "-4.0"

    assert Parser("(one two three :four -5.01 \"six and some more\")").parse_first().to_list()[4] == -5.01

    assert str(Parser("(if(and(one)(two))(three))").parse_first()) == "(if (and (one) (two)) (three))"