# ParserGenerator

## Authors:
- Kévin BEDIN
- Quentin DUCASSE

## Project definition

As part of our compilation course, we had to put together a `lexer`, `parser`,`ast`, `visitor` and `pretty printer` **for the language** of our choice, **in the language** of our choice. What we chose here is a **PYTHON-based EBNF compiler**. The *Extended Backus-Naur Form* (EBNF) is the language used to describe the syntax of any programming language. The objectives of our project are now:
* Define the **EBNF-Grammar**
* Write a **lexer** of this grammar
* Write a **parser** of the generated *lexems*
* Structure the *lexems* in an **Abstract Syntax Tree**
* Visit the abstract syntax tree with **visitors**
⋅⋅* **Lexer Writer** creating a lexer for the parsed grammar
⋅⋅* **Parser Writer** creating a parser for the parsed grammar
* Pretty print the grammar to double check everything went fine
	
## Grammar

The EBNF Grammar we used can be found inside the **ISO-14977** inside the `docs` directory. The grammar itself can be found under `parserGenerator/ebnf_grammar.ebnf`. This grammar will be the one defining how our **EBNF** **parser** & **lexer** work and how the **ast** is structured.

## Lexer & Parser Generation

The generation of the parsed grammar lexer and parser is made through Jinja templates that can be found under `parserGenerator/templates` and rendered inside the `parserWriter` and `lexerWriterV2`.

## Generator launching

Write the following command while in `parserGenerator` to launch the generator:
```
$ python3 testFile.py
```

that can be used with: 
* `testLexerWriterEBNF.py`
* `testLexerWriterPascal.py`
* `testLexerWriterPascal_v2.py`
* `testParserWriterCpp.py`
* `testParserWriterJava.py`
* `testParserWriterPascal.py`

Please remember to install `Jinja2` as it is our template render.
You can do so through 
```
$ pip install Jinja2
```
or 
```
$ easy_install Jinja2
```

The results of the tests can be found in the `results` directory.


