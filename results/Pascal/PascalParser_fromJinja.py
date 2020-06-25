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
        self.expect('PROGRAM')
        self.parseWhitespace()
        self.parseIdentifier()
        self.parseWhitespace()
        self.expect('BEGIN')
        self.parseWhitespace()
        while(self.testAssignment()):
            self.parseAssignment()
            self.expect(";")
            self.parseWhitespace()
            
        self.expect('END.')
        self.indentator.dedent()


    def testProgram(self):
        next=self.show_next().tag
        testing_list=['PROGRAM']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseIdentifier(self):
        self.indentator.indent('Parsing Identifier')
        self.parseAlphabeticcharacter()
        while(self.testAlphabeticcharacter() or self.testDigit()):
            if(self.testAlphabeticcharacter()):
                self.parseAlphabeticcharacter()
            elif(self.testDigit()):
                self.parseDigit()
                
            
        self.indentator.dedent()


    def testIdentifier(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testAlphabeticcharacter())
        return(test)


    def parseNumber(self):
        self.indentator.indent('Parsing Number')
        if(self.show_next().tag == "-"):
            self.expect("-")
            
        self.parseDigit()
        while(self.testDigit()):
            self.parseDigit()
            
        self.indentator.dedent()


    def testNumber(self):
        next=self.show_next().tag
        testing_list=['-']
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testDigit())
        return(test)


    def parseString(self):
        self.indentator.indent('Parsing String')
        self.expect('"')
        while(self.testAllcharacters()):
            self.parseAllcharacters()
            
        self.expect('"')
        self.indentator.dedent()


    def testString(self):
        next=self.show_next().tag
        testing_list=['"']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseAssignment(self):
        self.indentator.indent('Parsing Assignment')
        self.parseIdentifier()
        self.expect(":=")
        if(self.testNumber()):
            self.parseNumber()
        elif(self.testIdentifier()):
            self.parseIdentifier()
        elif(self.testString()):
            self.parseString()
            
        self.indentator.dedent()


    def testAssignment(self):
        next=self.show_next().tag
        testing_list=[]
        test=(next in testing_list)
        if (test): return(test)
        test=(test or self.testIdentifier())
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
            
        self.indentator.dedent()


    def testAlphabeticcharacter(self):
        next=self.show_next().tag
        testing_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
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


    def parseAllalphabeticcharacter(self):
        self.indentator.indent('Parsing Allalphabeticcharacter')
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


    def testAllalphabeticcharacter(self):
        next=self.show_next().tag
        testing_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseSpecialcharacter(self):
        self.indentator.indent('Parsing Specialcharacter')
        if(self.show_next().tag == "_"):
            self.expect("_")
        elif(self.show_next().tag == "!"):
            self.expect("!")
        elif(self.show_next().tag == "?"):
            self.expect("?")
            
        self.indentator.dedent()


    def testSpecialcharacter(self):
        next=self.show_next().tag
        testing_list=['_', '!', '?']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseWhitespace(self):
        self.indentator.indent('Parsing Whitespace')
        while(self.show_next().tag == " "):
            self.expect(" ")
            self.parseWhitespace()
            
        self.indentator.dedent()


    def testWhitespace(self):
        next=self.show_next().tag
        testing_list=[' ']
        test=(next in testing_list)
        if (test): return(test)
        return(test)


    def parseAllcharacters(self):
        self.indentator.indent('Parsing Allcharacters')
        if(self.testAllalphabeticcharacter()):
            self.parseAllalphabeticcharacter()
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
        test=(test or self.testAllalphabeticcharacter())
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