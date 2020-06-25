import sys
import copy
from ast    import *
from indent import Indent
from colors import Colors


class Parser:


    def __init__(self, verbose=False):
        '''
        Parser constructor
        ---
        Args:    boolean verbose
        Returns: None
        '''
        self.indentator = Indent(verbose)
        self.lexems = []
        self.errors = 0

    def show_next(self, n=1):
        '''
        Returns the next token in the list while not poping it output
        ---
        Args   : int n (optional) the index of the targetted token
        Returns: token with index n from the lexems list
        '''
        try:
            return self.lexems[n - 1]
        except IndexError:
            print('ERROR: no more lexems left!')
            sys.exit(1)

    def expect(self, tag):
        '''
        Pops the next token from the lexems list and tests its type
        ---
        Args   : string tag, the wanted tag
        Returns: next token from the list
        '''
        actualLexem = self.show_next()
        actualtag = actualLexem.tag
        actualPosition = actualLexem.position
        if actualtag == tag:
            return self.accept_it()
        else:
            print('Error at {}: expected {}, got {} instead'.format(str(actualPosition), tag, actualtag))
            sys.exit(1)

    # same as expect() but no error if not correct tag
    def maybe(self, tag):
        '''
        Pops the next token from the lexems list without raising error on its type
        ---
        Args   : string tag, the wanted tag
        Returns: next token from the list
        '''
        if self.show_next().tag == tag:
            return self.accept_it()

    def accept_it(self):
        '''

        '''
        token = self.show_next()
        output = Colors.FAIL + token.value + Colors.ENDC
        self.indentator.say(output)
        return self.lexems.pop(0)

    def remove_comments(self):
        '''
        Removes the comments from the token list
        ---
        Args:    None
        Return : None
        '''
        result = []
        for token in self.lexems:
            if token.tag == 'COMMENT':
                pass
            else:
                result.append(token)
        return result

    def remove_comments_whitespace(self):
        '''
        Removes the comments and the whitespaces from the token list
        ---
        Args:    None
        Return : None
        '''
        result = []
        for token in self.lexems:
            if token.tag == 'COMMENT' or token.value==" ":
                pass
            else:
                result.append(token)
        return result
        

    def parseProgram(self):
        self.indentator.indent('Parsing Program')
        while(self.testInclude()):
            self.parseInclude()
            
        while(self.testRaccourci()):
            self.parseRaccourci()
            
        self.parseMain()
        self.indentator.dedent()


    def testProgram(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testInclude())
        return(test)


    def parseInclude(self):
        self.indentator.indent('Parsing Include')
        self.expect("#include")
        self.expect("<")
        self.parseIdentifier()
        self.expect(">")
        self.indentator.dedent()


    def testInclude(self):
        next=self.show_next().tag
        testing_list=['#include']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseRaccourci(self):
        self.indentator.indent('Parsing Raccourci')
        self.expect("using")
        self.expect("namespace")
        self.parseIdentifier()
        self.expect(";")
        self.indentator.dedent()


    def testRaccourci(self):
        next=self.show_next().tag
        testing_list=['using']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseNumber(self):
        self.indentator.indent('Parsing Number')
        if(self.testInteger()):
            self.parseInteger()
        elif(self.testDoublenumber()):
            self.parseDoublenumber()
            
        self.indentator.dedent()


    def testNumber(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testInteger())
        test=(test or self.testDoublenumber())
        return(test)


    def parseType(self):
        self.indentator.indent('Parsing Type')
        if(self.show_next().tag == "int"):
            self.expect("int")
        elif(self.show_next().tag == "double"):
            self.expect("double")
            
        self.indentator.dedent()


    def testType(self):
        next=self.show_next().tag
        testing_list=['int', 'double']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseTerm(self):
        self.indentator.indent('Parsing Term')
        if(self.show_next().tag == "-"):
            self.expect("-")
            
        if(self.testIdentifier()):
            self.parseIdentifier()
        elif(self.testNumber()):
            self.parseNumber()
            
        self.indentator.dedent()


    def testTerm(self):
        next=self.show_next().tag
        testing_list=['-']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIdentifier())
        test=(test or self.testNumber())
        return(test)


    def parseFonctionmath(self):
        self.indentator.indent('Parsing Fonctionmath')
        if(self.show_next().tag == "cos"):
            self.expect("cos")
        elif(self.show_next().tag == "sin"):
            self.expect("sin")
        elif(self.show_next().tag == "pow"):
            self.expect("pow")
        elif(self.show_next().tag == "sqrt"):
            self.expect("sqrt")
            
        self.indentator.dedent()


    def testFonctionmath(self):
        next=self.show_next().tag
        testing_list=['cos', 'sin', 'pow', 'sqrt']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseFonction(self):
        self.indentator.indent('Parsing Fonction')
        self.parseFonctionmath()
        self.expect("(")
        self.parseExpression()
        while(self.show_next().tag == ","):
            self.expect(",")
            self.parseExpression()
            
        self.expect(")")
        self.indentator.dedent()


    def testFonction(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testFonctionmath())
        return(test)


    def parseStd(self):
        self.indentator.indent('Parsing Std')
        self.expect("std::")
        self.indentator.dedent()


    def testStd(self):
        next=self.show_next().tag
        testing_list=['std::']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseFonctionprint(self):
        self.indentator.indent('Parsing Fonctionprint')
        if(self.testStd()):
            self.parseStd()
            
        self.expect("cout")
        if(self.show_next().tag == "<<"):
            self.expect("<<")
        elif(self.show_next().tag == "<"):
            self.expect("<")
            self.expect("<")
            
        self.parseExpression()
        if(self.show_next().tag == "<<"):
            self.expect("<<")
        elif(self.show_next().tag == "<"):
            self.expect("<")
            self.expect("<")
            
        while(self.testExpression()):
            self.parseExpression()
            if(self.show_next().tag == "<<"):
                self.expect("<<")
            elif(self.show_next().tag == "<"):
                self.expect("<")
                self.expect("<")
                
            
        if(self.testStd()):
            self.parseStd()
            
        self.expect("endl")
        self.indentator.dedent()


    def testFonctionprint(self):
        next=self.show_next().tag
        testing_list=['cout']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testStd())
        return(test)


    def parseSimpleexpression(self):
        self.indentator.indent('Parsing Simpleexpression')
        if(self.testFonction()):
            self.parseFonction()
        elif(self.testTerm()):
            self.parseTerm()
        elif(self.testString()):
            self.parseString()
            
        self.indentator.dedent()


    def testSimpleexpression(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testFonction())
        test=(test or self.testTerm())
        test=(test or self.testString())
        return(test)


    def parseExpression(self):
        self.indentator.indent('Parsing Expression')
        self.parseSimpleexpression()
        while(self.show_next().tag == "==" or self.show_next().tag == "=" or self.show_next().tag == "+" or self.show_next().tag == ":" or self.show_next().tag == ":" or self.show_next().tag == "-" or self.show_next().tag == "<" or self.show_next().tag == ">" or self.show_next().tag == "<=" or self.show_next().tag == ">=" or self.show_next().tag == "/" or self.show_next().tag == "*"):
            if(self.show_next().tag == "=="):
                self.expect("==")
            elif(self.show_next().tag == "="):
                self.expect("=")
            elif(self.show_next().tag == "+"):
                self.expect("+")
            elif(self.show_next().tag == ":"):
                self.expect(":")
                self.expect(":")
            elif(self.show_next().tag == "-"):
                self.expect("-")
            elif(self.show_next().tag == "<"):
                self.expect("<")
            elif(self.show_next().tag == ">"):
                self.expect(">")
            elif(self.show_next().tag == "<="):
                self.expect("<=")
            elif(self.show_next().tag == ">="):
                self.expect(">=")
            elif(self.show_next().tag == "/"):
                self.expect("/")
            elif(self.show_next().tag == "*"):
                self.expect("*")
                
            self.parseSimpleexpression()
            
        self.indentator.dedent()


    def testExpression(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testSimpleexpression())
        return(test)


    def parseExpressionc(self):
        self.indentator.indent('Parsing Expressionc')
        if(self.testFonctionprint()):
            self.parseFonctionprint()
        elif(self.testExpression()):
            self.parseExpression()
            
        self.expect(";")
        self.indentator.dedent()


    def testExpressionc(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testFonctionprint())
        test=(test or self.testExpression())
        return(test)


    def parseAssignment(self):
        self.indentator.indent('Parsing Assignment')
        self.parseType()
        self.parseIdentifier()
        while(self.show_next().tag == ","):
            self.expect(",")
            self.parseIdentifier()
            
        self.expect("=")
        self.parseExpression()
        self.expect(";")
        self.indentator.dedent()


    def testAssignment(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testType())
        return(test)


    def parseIfstatement(self):
        self.indentator.indent('Parsing Ifstatement')
        self.expect("if")
        self.expect("(")
        self.parseExpression()
        self.expect(")")
        if(self.show_next().tag == "{"):
            self.expect("{")
            
        while(self.testStatement()):
            self.parseStatement()
            
        if(self.show_next().tag == "}"):
            self.expect("}")
            
        if(self.show_next().tag == "else if"):
            self.expect("else if")
            self.expect("(")
            self.parseExpression()
            self.expect(")")
            if(self.show_next().tag == "{"):
                self.expect("{")
                
            while(self.testStatement()):
                self.parseStatement()
                
            if(self.show_next().tag == "}"):
                self.expect("}")
                
            
        if(self.show_next().tag == "else"):
            self.expect("else")
            self.expect("{")
            while(self.testStatement()):
                self.parseStatement()
                
            self.expect("}")
            
        self.indentator.dedent()


    def testIfstatement(self):
        next=self.show_next().tag
        testing_list=['if']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseForstatement(self):
        self.indentator.indent('Parsing Forstatement')
        self.expect("for")
        self.expect("(")
        self.parseStatement()
        self.parseExpressionc()
        self.parseExpression()
        self.expect(")")
        if(self.show_next().tag == "{"):
            self.expect("{")
            
        while(self.testStatement()):
            self.parseStatement()
            
        if(self.show_next().tag == "}"):
            self.expect("}")
            
        self.indentator.dedent()


    def testForstatement(self):
        next=self.show_next().tag
        testing_list=['for']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseWhilestatement(self):
        self.indentator.indent('Parsing Whilestatement')
        self.expect("while")
        self.expect("(")
        self.parseExpression()
        self.expect(")")
        if(self.show_next().tag == "{"):
            self.expect("{")
            
        while(self.testStatement()):
            self.parseStatement()
            
        if(self.show_next().tag == "}"):
            self.expect("}")
            
        self.indentator.dedent()


    def testWhilestatement(self):
        next=self.show_next().tag
        testing_list=['while']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseReturn(self):
        self.indentator.indent('Parsing Return')
        self.expect("return")
        self.parseExpressionc()
        self.indentator.dedent()


    def testReturn(self):
        next=self.show_next().tag
        testing_list=['return']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseStatement(self):
        self.indentator.indent('Parsing Statement')
        if(self.testIfstatement()):
            self.parseIfstatement()
        elif(self.testForstatement()):
            self.parseForstatement()
        elif(self.testWhilestatement()):
            self.parseWhilestatement()
        elif(self.testReturn()):
            self.parseReturn()
        elif(self.testAssignment()):
            self.parseAssignment()
        elif(self.testExpressionc()):
            self.parseExpressionc()
            
        self.indentator.dedent()


    def testStatement(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIfstatement())
        test=(test or self.testForstatement())
        test=(test or self.testWhilestatement())
        test=(test or self.testReturn())
        test=(test or self.testAssignment())
        test=(test or self.testExpressionc())
        return(test)


    def parseDeclaremethode(self):
        self.indentator.indent('Parsing Declaremethode')
        self.parseType()
        self.parseIdentifier()
        self.expect("(")
        if(self.testType()):
            self.parseType()
            self.parseIdentifier()
            while(self.show_next().tag == ","):
                self.expect(",")
                self.parseType()
                self.parseIdentifier()
                
            
        self.expect(")")
        self.indentator.dedent()


    def testDeclaremethode(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testType())
        return(test)


    def parseMethode(self):
        self.indentator.indent('Parsing Methode')
        self.parseDeclaremethode()
        self.expect("{")
        while(self.testStatement()):
            self.parseStatement()
            
        self.expect("}")
        self.indentator.dedent()


    def testMethode(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testDeclaremethode())
        return(test)


    def parseMain(self):
        self.indentator.indent('Parsing Main')
        self.parseType()
        self.expect("main")
        self.expect("(")
        if(self.testType()):
            self.parseType()
            self.parseIdentifier()
            while(self.show_next().tag == ","):
                self.expect(",")
                self.parseType()
                self.parseIdentifier()
                
            
        self.expect(")")
        self.expect("{")
        while(self.testStatement()):
            self.parseStatement()
            
        self.expect("}")
        self.indentator.dedent()


    def testMain(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testType())
        return(test)


    def parseLetter(self):
        self.indentator.indent('Parsing Letter')
        if(self.show_next().tag == "A"):
            self.expect("A")
        elif(self.show_next().tag == "B"):
            self.expect("B")
        elif(self.show_next().tag == "C"):
            self.expect("C")
        elif(self.show_next().tag == "D"):
            self.expect("D")
        elif(self.show_next().tag == "E"):
            self.expect("E")
        elif(self.show_next().tag == "F"):
            self.expect("F")
        elif(self.show_next().tag == "G"):
            self.expect("G")
        elif(self.show_next().tag == "H"):
            self.expect("H")
        elif(self.show_next().tag == "I"):
            self.expect("I")
        elif(self.show_next().tag == "J"):
            self.expect("J")
        elif(self.show_next().tag == "K"):
            self.expect("K")
        elif(self.show_next().tag == "L"):
            self.expect("L")
        elif(self.show_next().tag == "M"):
            self.expect("M")
        elif(self.show_next().tag == "N"):
            self.expect("N")
        elif(self.show_next().tag == "O"):
            self.expect("O")
        elif(self.show_next().tag == "P"):
            self.expect("P")
        elif(self.show_next().tag == "Q"):
            self.expect("Q")
        elif(self.show_next().tag == "R"):
            self.expect("R")
        elif(self.show_next().tag == "S"):
            self.expect("S")
        elif(self.show_next().tag == "T"):
            self.expect("T")
        elif(self.show_next().tag == "U"):
            self.expect("U")
        elif(self.show_next().tag == "V"):
            self.expect("V")
        elif(self.show_next().tag == "W"):
            self.expect("W")
        elif(self.show_next().tag == "X"):
            self.expect("X")
        elif(self.show_next().tag == "Y"):
            self.expect("Y")
        elif(self.show_next().tag == "Z"):
            self.expect("Z")
        elif(self.show_next().tag == "a"):
            self.expect("a")
        elif(self.show_next().tag == "b"):
            self.expect("b")
        elif(self.show_next().tag == "c"):
            self.expect("c")
        elif(self.show_next().tag == "d"):
            self.expect("d")
        elif(self.show_next().tag == "e"):
            self.expect("e")
        elif(self.show_next().tag == "f"):
            self.expect("f")
        elif(self.show_next().tag == "g"):
            self.expect("g")
        elif(self.show_next().tag == "h"):
            self.expect("h")
        elif(self.show_next().tag == "i"):
            self.expect("i")
        elif(self.show_next().tag == "j"):
            self.expect("j")
        elif(self.show_next().tag == "k"):
            self.expect("k")
        elif(self.show_next().tag == "l"):
            self.expect("l")
        elif(self.show_next().tag == "m"):
            self.expect("m")
        elif(self.show_next().tag == "n"):
            self.expect("n")
        elif(self.show_next().tag == "o"):
            self.expect("o")
        elif(self.show_next().tag == "p"):
            self.expect("p")
        elif(self.show_next().tag == "q"):
            self.expect("q")
        elif(self.show_next().tag == "r"):
            self.expect("r")
        elif(self.show_next().tag == "s"):
            self.expect("s")
        elif(self.show_next().tag == "t"):
            self.expect("t")
        elif(self.show_next().tag == "u"):
            self.expect("u")
        elif(self.show_next().tag == "v"):
            self.expect("v")
        elif(self.show_next().tag == "w"):
            self.expect("w")
        elif(self.show_next().tag == "x"):
            self.expect("x")
        elif(self.show_next().tag == "y"):
            self.expect("y")
        elif(self.show_next().tag == "z"):
            self.expect("z")
            
        self.indentator.dedent()


    def testLetter(self):
        next=self.show_next().tag
        testing_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseDigit(self):
        self.indentator.indent('Parsing Digit')
        if(self.show_next().tag == "0"):
            self.expect("0")
        elif(self.show_next().tag == "1"):
            self.expect("1")
        elif(self.show_next().tag == "2"):
            self.expect("2")
        elif(self.show_next().tag == "3"):
            self.expect("3")
        elif(self.show_next().tag == "4"):
            self.expect("4")
        elif(self.show_next().tag == "5"):
            self.expect("5")
        elif(self.show_next().tag == "6"):
            self.expect("6")
        elif(self.show_next().tag == "7"):
            self.expect("7")
        elif(self.show_next().tag == "8"):
            self.expect("8")
        elif(self.show_next().tag == "9"):
            self.expect("9")
            
        self.indentator.dedent()


    def testDigit(self):
        next=self.show_next().tag
        testing_list=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseWhitespace(self):
        self.indentator.indent('Parsing Whitespace')
        self.expect(" ")
        self.indentator.dedent()


    def testWhitespace(self):
        next=self.show_next().tag
        testing_list=[' ']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseInteger(self):
        self.indentator.indent('Parsing Integer')
        self.parseDigit()
        while(self.testDigit()):
            self.parseDigit()
            
        self.indentator.dedent()


    def testInteger(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testDigit())
        return(test)


    def parseDoublenumber(self):
        self.indentator.indent('Parsing Doublenumber')
        self.parseDigit()
        while(self.testDigit()):
            self.parseDigit()
            
        if(self.show_next().tag == "."):
            self.expect(".")
            self.parseDigit()
            while(self.testDigit()):
                self.parseDigit()
                
            
        self.indentator.dedent()


    def testDoublenumber(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testDigit())
        return(test)


    def parseIdentifier(self):
        self.indentator.indent('Parsing Identifier')
        self.parseLetter()
        while(self.testLetter() or self.testDigit()):
            if(self.testLetter()):
                self.parseLetter()
            elif(self.testDigit()):
                self.parseDigit()
                
            
        self.indentator.dedent()


    def testIdentifier(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testLetter())
        return(test)


    def parseString(self):
        self.indentator.indent('Parsing String')
        self.expect('"')
        self.parseAllcharacters()
        self.expect('"')
        self.indentator.dedent()


    def testString(self):
        next=self.show_next().tag
        testing_list=['"']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseSpecialcharacter(self):
        self.indentator.indent('Parsing Specialcharacter')
        if(self.show_next().tag == "?"):
            self.expect("?")
        elif(self.show_next().tag == "_"):
            self.expect("_")
        elif(self.show_next().tag == "!"):
            self.expect("!")
            
        self.indentator.dedent()


    def testSpecialcharacter(self):
        next=self.show_next().tag
        testing_list=['?', '_', '!']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseAllcharacters(self):
        self.indentator.indent('Parsing Allcharacters')
        while(self.testLetter() or self.testWhitespace() or self.testSpecialcharacter()):
            if(self.testLetter()):
                self.parseLetter()
            elif(self.testWhitespace()):
                self.parseWhitespace()
            elif(self.testSpecialcharacter()):
                self.parseSpecialcharacter()
                
            
        self.indentator.dedent()


    def testAllcharacters(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testLetter())
        test=(test or self.testWhitespace())
        test=(test or self.testSpecialcharacter())
        return(test)

    def parse(self, lexems, remove_comments_whitespace=False):
        '''
        Main function: launches the parsing operation
        ---
        Args:
        Returns
        '''
        self.lexems = lexems
        #print(self.lexems)
        if remove_comments_whitespace:
            self.lexems = self.remove_comments_whitespace()
        else:
            self.lexems = self.remove_comments()
        self.parseProgram()