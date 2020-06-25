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
        

    def parseGoal(self):
        self.indentator.indent('Parsing Goal')
        self.parseMainclass()
        while(self.testClassdeclaration()):
            self.parseClassdeclaration()
            
        self.parseEof()
        self.indentator.dedent()


    def testGoal(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testMainclass())
        return(test)


    def parseMainclass(self):
        self.indentator.indent('Parsing Mainclass')
        self.expect("class")
        self.parseIdentifier()
        self.expect("{")
        self.expect("public")
        self.expect("static")
        self.expect("void")
        self.expect("main")
        self.expect("(")
        self.expect("String")
        self.expect("[")
        self.expect("]")
        self.parseIdentifier()
        self.expect(")")
        self.expect("{")
        self.parseStatement()
        self.expect("}")
        self.expect("}")
        self.indentator.dedent()


    def testMainclass(self):
        next=self.show_next().tag
        testing_list=['class']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseClassdeclaration(self):
        self.indentator.indent('Parsing Classdeclaration')
        self.expect("class")
        self.parseIdentifier()
        if(self.show_next().tag == "extends"):
            self.expect("extends")
            self.parseIdentifier()
            
        self.expect("{")
        while(self.testVardeclaration()):
            self.parseVardeclaration()
            
        while(self.testMethoddeclaration()):
            self.parseMethoddeclaration()
            
        self.expect("}")
        self.indentator.dedent()


    def testClassdeclaration(self):
        next=self.show_next().tag
        testing_list=['class']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseVardeclaration(self):
        self.indentator.indent('Parsing Vardeclaration')
        self.parseType()
        self.parseIdentifier()
        self.expect(";")
        self.indentator.dedent()


    def testVardeclaration(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testType())
        return(test)


    def parseMethoddeclaration(self):
        self.indentator.indent('Parsing Methoddeclaration')
        self.expect("public")
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
        self.expect("{")
        while(self.testVardeclaration()):
            self.parseVardeclaration()
            
        while(self.testStatement()):
            self.parseStatement()
            
        self.expect("return")
        self.parseExpression()
        self.expect(";")
        self.expect("}")
        self.indentator.dedent()


    def testMethoddeclaration(self):
        next=self.show_next().tag
        testing_list=['public']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseType(self):
        self.indentator.indent('Parsing Type')
        if(self.show_next().tag == "int"):
            self.expect("int")
            if(self.show_next().tag == "["):
                self.expect("[")
                self.expect("]")
                
        elif(self.show_next().tag == "boolean"):
            self.expect("boolean")
        elif(self.testIdentifier()):
            self.parseIdentifier()
            
        self.indentator.dedent()


    def testType(self):
        next=self.show_next().tag
        testing_list=['int', 'boolean']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIdentifier())
        return(test)


    def parseStatement(self):
        self.indentator.indent('Parsing Statement')
        if(self.show_next().tag == "{"):
            self.expect("{")
            while(self.testStatement()):
                self.parseStatement()
                
            self.expect("}")
        elif(self.show_next().tag == "if"):
            self.expect("if")
            self.expect("(")
            self.parseExpression()
            self.expect(")")
            self.parseStatement()
            self.expect("else")
            self.parseStatement()
        elif(self.show_next().tag == "while"):
            self.expect("while")
            self.expect("(")
            self.parseExpression()
            self.expect(")")
            self.parseStatement()
        elif(self.show_next().tag == "System.out.println"):
            self.expect("System.out.println")
            self.expect("(")
            self.parseExpression()
            self.expect(")")
            self.expect(";")
        elif(self.testIdentifier()):
            self.parseIdentifier()
            self.expect("=")
            self.parseExpression()
            self.expect(";")
        elif(self.testIdentifier()):
            self.parseIdentifier()
            self.expect("[")
            self.parseExpression()
            self.expect("]")
            self.expect("=")
            self.parseExpression()
            self.expect(";")
            
        self.indentator.dedent()


    def testStatement(self):
        next=self.show_next().tag
        testing_list=['{', 'if', 'while', 'System.out.println']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIdentifier())
        test=(test or self.testIdentifier())
        return(test)


    def parseExpression(self):
        self.indentator.indent('Parsing Expression')
        if(self.testExpression1()):
            self.parseExpression1()
        elif(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testIdentifier()):
            self.parseIdentifier()
        elif(self.testSpecial()):
            self.parseSpecial()
        elif(self.show_next().tag == "!"):
            self.expect("!")
            self.parseExpression()
        elif(self.show_next().tag == "("):
            self.expect("(")
            self.parseExpression()
            self.expect(")")
        elif(self.testExpression2()):
            self.parseExpression2()
        elif(self.testExpression3()):
            self.parseExpression3()
        elif(self.testExpression4()):
            self.parseExpression4()
            
        self.indentator.dedent()


    def testExpression(self):
        next=self.show_next().tag
        testing_list=['!', '(']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression1())
        test=(test or self.testIntegerliteral())
        test=(test or self.testIdentifier())
        test=(test or self.testSpecial())
        test=(test or self.testExpression2())
        test=(test or self.testExpression3())
        test=(test or self.testExpression4())
        return(test)


    def parseExpression1(self):
        self.indentator.indent('Parsing Expression1')
        if(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testIdentifier()):
            self.parseIdentifier()
            
        if(self.show_next().tag == "&&" or self.show_next().tag == "<" or self.show_next().tag == "+" or self.show_next().tag == "-" or self.show_next().tag == "*"):
            if(self.show_next().tag == "&&"):
                self.expect("&&")
            elif(self.show_next().tag == "<"):
                self.expect("<")
            elif(self.show_next().tag == "+"):
                self.expect("+")
            elif(self.show_next().tag == "-"):
                self.expect("-")
            elif(self.show_next().tag == "*"):
                self.expect("*")
                
            
        if(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testIdentifier()):
            self.parseIdentifier()
        elif(self.testBool()):
            self.parseBool()
        elif(self.testSpecial()):
            self.parseSpecial()
        elif(self.testExpression5()):
            self.parseExpression5()
            
        self.indentator.dedent()


    def testExpression1(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIntegerliteral())
        test=(test or self.testIdentifier())
        test=(test or self.testIntegerliteral())
        test=(test or self.testIdentifier())
        test=(test or self.testBool())
        test=(test or self.testSpecial())
        test=(test or self.testExpression5())
        return(test)


    def parseExpression2(self):
        self.indentator.indent('Parsing Expression2')
        self.parseExpression()
        self.expect("[")
        self.parseExpression()
        self.expect("]")
        self.indentator.dedent()


    def testExpression2(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression3(self):
        self.indentator.indent('Parsing Expression3')
        self.parseExpression()
        self.expect(".")
        self.expect("length")
        self.indentator.dedent()


    def testExpression3(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression4(self):
        self.indentator.indent('Parsing Expression4')
        self.parseExpression()
        if(self.show_next().tag == "("):
            self.expect("(")
            if(self.testExpression1()):
                self.parseExpression1()
                
            self.expect(")")
            
        self.expect(".")
        self.parseIdentifier()
        self.expect("(")
        if(self.testExpression()):
            self.parseExpression()
            while(self.show_next().tag == ","):
                self.expect(",")
                self.parseExpression()
                
            
        self.expect(")")
        self.indentator.dedent()


    def testExpression4(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression5(self):
        self.indentator.indent('Parsing Expression5')
        self.expect("new")
        if(self.show_next().tag == "int"):
            self.expect("int")
            self.expect("[")
            self.parseExpression()
            self.expect("]")
        elif(self.testExpression4()):
            self.parseExpression4()
            
        self.indentator.dedent()


    def testExpression5(self):
        next=self.show_next().tag
        testing_list=['new']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseExpression6(self):
        self.indentator.indent('Parsing Expression6')
        self.parseExpression()
        self.parseExpression7()
        self.indentator.dedent()


    def testExpression6(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testExpression())
        return(test)


    def parseExpression7(self):
        self.indentator.indent('Parsing Expression7')
        if(self.show_next().tag == "("):
            self.expect("(")
            if(self.testExpression()):
                self.parseExpression()
                
            self.expect(")")
            
        self.indentator.dedent()


    def testExpression7(self):
        next=self.show_next().tag
        testing_list=['(']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseBool(self):
        self.indentator.indent('Parsing Bool')
        if(self.show_next().tag == "true"):
            self.expect("true")
        elif(self.show_next().tag == "false"):
            self.expect("false")
            
        self.indentator.dedent()


    def testBool(self):
        next=self.show_next().tag
        testing_list=['true', 'false']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseSpecial(self):
        self.indentator.indent('Parsing Special')
        self.expect("this")
        if(self.show_next().tag == "."):
            self.expect(".")
            
        if(self.testExpression6()):
            self.parseExpression6()
            
        self.indentator.dedent()


    def testSpecial(self):
        next=self.show_next().tag
        testing_list=['this']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseAlphabeticcharacter(self):
        self.indentator.indent('Parsing Alphabeticcharacter')
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


    def testAlphabeticcharacter(self):
        next=self.show_next().tag
        testing_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseSpecialcharacter(self):
        self.indentator.indent('Parsing Specialcharacter')
        self.expect("_")
        self.indentator.dedent()


    def testSpecialcharacter(self):
        next=self.show_next().tag
        testing_list=['_']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseWhitespace(self):
        self.indentator.indent('Parsing Whitespace')
        self.expect(" ")
        while(self.testWhitespace()):
            self.parseWhitespace()
            
        self.indentator.dedent()


    def testWhitespace(self):
        next=self.show_next().tag
        testing_list=[' ']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseIdentifier(self):
        self.indentator.indent('Parsing Identifier')
        if(self.testAllcharacters()):
            self.parseAllcharacters()
        elif(self.testIntegerliteral()):
            self.parseIntegerliteral()
        elif(self.testWhitespace()):
            self.parseWhitespace()
        elif(self.testSpecialcharacter()):
            self.parseSpecialcharacter()
            
        while(self.testAllcharacters() or self.testIntegerliteral() or self.testWhitespace() or self.testSpecialcharacter()):
            if(self.testAllcharacters()):
                self.parseAllcharacters()
            elif(self.testIntegerliteral()):
                self.parseIntegerliteral()
            elif(self.testWhitespace()):
                self.parseWhitespace()
            elif(self.testSpecialcharacter()):
                self.parseSpecialcharacter()
                
            
        self.indentator.dedent()


    def testIdentifier(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testAllcharacters())
        test=(test or self.testIntegerliteral())
        test=(test or self.testWhitespace())
        test=(test or self.testSpecialcharacter())
        return(test)


    def parseAllcharacters(self):
        self.indentator.indent('Parsing Allcharacters')
        self.parseAlphabeticcharacter()
        self.indentator.dedent()


    def testAllcharacters(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testAlphabeticcharacter())
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


    def parseIntegerliteral(self):
        self.indentator.indent('Parsing Integerliteral')
        self.parseDigit()
        while(self.testDigit()):
            self.parseDigit()
            
        self.indentator.dedent()


    def testIntegerliteral(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testDigit())
        return(test)


    def parseEof(self):
        self.indentator.indent('Parsing Eof')
        self.expect(".")
        self.indentator.dedent()


    def testEof(self):
        next=self.show_next().tag
        testing_list=['.']
        test=(next in testing_list)
        if (test): return(test)
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
        self.parseGoal()