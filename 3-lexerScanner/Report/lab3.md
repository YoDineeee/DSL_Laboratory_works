# Lexer & Scanner

### Course: Formal Languages & Finite Automata  
### Author: Mohamed Dhiaeddir hassine , st.gr.FAF-233  
### Verified by: Dumitru Crețu, University Assistant  

----

## Theoretical Background

### Lexical Analysis and Tokenization

Lexical analysis, or scanning, is the initial phase in the compilation or interpretation process. It involves converting a raw text input into a sequence of meaningful symbols called **tokens**, which serve as atomic units of syntax.

Important definitions include:

- **Token**: A class representing categories like keywords, identifiers, literals, or symbols.
- **Lexeme**: A specific substring from the source text that matches a token pattern.
- **Pattern**: A regular expression describing how to identify each token.

### Purpose of the Lexer

A lexer plays a key role in any compiler or interpreter pipeline by:

1. **Breaking down source code** into atomic, structured units (tokens).
2. **Removing irrelevant characters**, such as whitespace and comments.
3. **Providing context** (like line/column numbers) to help parsers and error handlers.
4. **Improving maintainability**, as separating tokenization simplifies parser implementation.

### Regular Expressions in Tokenization

Lexers often use **regular expressions** to describe token patterns. These expressions make it possible to flexibly and precisely identify:

- Keywords like `PROCESS`, `STEP`, `TIME`, etc.
- Identifiers like `"engine"` or `"wheel assemblies"`
- Numeric values and units such as `1000`, `C`, `days`

## Objectives

This laboratory work focused on:

1. Understanding lexical analysis as a compilation stage.
2. Implementing a lexer for a process-oriented DSL (domain-specific language).
3. Utilizing regular expressions for token identification.
4. Tracking line and column numbers to support error localization.
5. Demonstrating correct behavior with a real-world process sample.

---

## Implementation Description

### DSL Specification

This lexer targets a structured DSL for modeling mass production processes. Key elements include:

- `PROCESS`: Start of a process block
- `TITLE`: Name of the process
- `YIELD`: Output quantity
- `TIME`: Duration of the process
- `COMPONENT`: Required materials
- `STEP`: Steps in the production
- `TEMP`: Processing temperature

### Lexer Class

The core component is the `Lexer` class in `Lexer.py`. It defines token patterns and performs scanning using regular expressions:

```python
self.token_patterns = {
    'KEYWORD': r'(PROCESS|TITLE|YIELD|TIME|COMPONENT|STEP|TEMP)',
    'STRING': r'"[^"]*"',
    'NUMBER': r'[0-9]+(\.[0-9]+)?',
    'UNIT': r'(g|ml|tsp|tbsp|cup|vehicles)',
    'TIME_UNIT': r'(min|hr|day|days)',
    'TEMP_UNIT': r'(C|F)',
    'ID': r'[a-zA-Z][a-zA-Z0-9_]*',
    'COLON': r':',
    'SEMICOLON': r';',
    'COMMA': r',',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'WHITESPACE': r'[ \t]+',
    'NEWLINE': r'\n'
}
```