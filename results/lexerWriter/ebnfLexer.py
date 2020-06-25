import re
import sys

class Lexem:

    def __init__(self, tag, value, position):
        self.tag = tag
        self.value = value
        self.position = position

    def __repr__(self):
        return self.tag

class LexerTemplate:

    regexExpressions = [
        (r'[\n]+',None),
        (r'\=','ASSIGN'),
        (r'\;','SEMICOLON'),
        (r'\|','PIPE'),
        (r'\,','COMMA'),
        (r'\-','SUB'),
        (r'\*','MUL'),
        (r'^\[$','LBRACKET'),
        (r'\]','RBRACKET'),
        (r'\{','LBRACE'),
        (r'\}','RBRACE'),
        (r'\(','LPAREN'),
        (r'\)','RPAREN'),
        (r'\?','INTERROGATION'),
        (r'\'','SQUOTE'),
        (r'\"','DQUOTE'),
        (r'\\','BSLASH')]

    def __init__(self):
        self.lexems = []


    def lex(self, inputText):
        lineNumber = 0
        for line in inputText:
            lineNumber += 1
            position = 0
            while position < len(line):
                match = None
                for tokenRegex in self.regexExpressions:
                    pattern, tag = tokenRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        if tag:
                            token = Lexem(tag, data, [lineNumber, position])
                            self.lexems.append(token)
                        break
                if not match:
                    print(line[position])
                    print("No match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("Lexer: analysis successful!")
        return self.lexems
