# Laboratory Work Report:Parser & Building an AST

### Course: Formal Languages & Finite Automata
### Author: Mohamed Dhiaeddine Hassine , st.gr.FAF-233
### Verified by: Dumitru Crețu, University Assistant

## Theory
**Domain-Specific Languages (DSLs)** are custom languages designed for specific tasks :

1. Lexical Analysis: Converting source code into tokens
2. Parsing: Creating an Abstract Syntax Tree (AST) from tokens
3. Abstract Syntax Tree: In-memory representation of the program structure
4. Visualization: Displaying the AST to understand the structure

## Objectives:


1. Understand what DSLs are and their purpose  
2. Create a lexer and parser for a Process DSL  
3. Build and represent the AST  
4. Visualize the AST structure

## Implementation Description
### Lexical Analysis
The lexer splits the input text into tokens by matching patterns for keywords, literals, and symbols.  
In the Process DSL, token types are defined using `Enum`, and regular expressions are used for pattern matching.


```python
class TokenType(Enum):
    # Keywords
    PROCESS = auto()
    TITLE = auto()
    COMPONENT = auto()
    STEP = auto()
    YIELD = auto()
    TIME = auto()
    TEMP = auto()
    # Literals
    STRING = auto()
    NUMBER = auto()
    # Units
    UNIT = auto()
    TIME_UNIT = auto()
    TEMP_UNIT = auto()
    # Symbols
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    LBRACE = auto()
    RBRACE = auto()
    ID = auto()

    # Special
    EOF = auto()
```
The Lexer class implements the tokenization process using regular expressions to match patterns in the input text:
```python
  def tokenize(self, text):
        self.tokens = []
        position = 0

        while position < len(text):
            match_found = False

            for token_type, pattern in self.token_patterns:
                regex = re.compile(f'^{pattern}', re.IGNORECASE)
                match = regex.match(text[position:])

                if match:
                    value = match.group(0)

                    if token_type is not None:  # Skip whitespace
                        self.tokens.append(Token(token_type, value))

                    position += len(value)
                    match_found = True
                    break

            if not match_found:
                raise ValueError(f"Unrecognized token at position {position}: '{text[position:position + 10]}'")

        self.tokens.append(Token(TokenType.EOF, ''))
        return self.tokens

```
This method scans the input text character by character, attempting to match token patterns. When a match is found, it creates a token with the appropriate type and value, then advances the position. This process continues until the entire input is processed.
### Abstract Syntax Tree (AST)

The AST represents the hierarchical structure of the Process. We define several node types to represent different elements of a Process:
```python
class ProcessNode:
    def __init__(self):
        self.title = None
        self.yield_node = None
        self.time_node = None
        self.components = []  # Initialize as empty list
        self.steps = []       # Initialize as empty list
        self.temperature = None

```
Other node types include ComponentNode, StepNode, TimeNode, TemperatureNode, etc., each capturing specific aspects of the Process structure.
### Parsing
The parser converts the sequence of tokens into an AST. It implements recursive descent parsing, where each grammar rule is represented by a parsing method:
```python
 def parse_process(self):
        # Expect PROCESS token
        self.consume(TokenType.PROCESS)
        self.consume(TokenType.LBRACE)

        # Initialize an empty PROCESS node
        process = ProcessNode()

        # Parse process components until we hit the closing brace
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.check(TokenType.TITLE):
                self.consume(TokenType.TITLE)
                self.consume(TokenType.COLON)
                title_value = self.consume(TokenType.STRING).value.strip('"')
                self.consume(TokenType.SEMICOLON)
                process.title = TitleNode(StringNode(title_value))

            elif self.check(TokenType.YIELD):
                self.consume(TokenType.YIELD)
                self.consume(TokenType.COLON)
                yield_value = float(self.consume(TokenType.NUMBER).value)
                self.consume(TokenType.SEMICOLON)
                process.yield_node = YieldNode(NumberNode(yield_value))

            elif self.check(TokenType.TIME):
                self.consume(TokenType.TIME)
                self.consume(TokenType.COLON)
                time_value = float(self.consume(TokenType.NUMBER).value)
                time_unit = self.consume(TokenType.TIME_UNIT).value
                self.consume(TokenType.SEMICOLON)
                process.time_node = TimeNode(NumberNode(time_value), UnitNode(time_unit))

            elif self.check(TokenType.COMPONENT):  # Changed here
                self.consume(TokenType.COMPONENT)   # Changed here
                self.consume(TokenType.COLON)

                quantity = NumberNode(float(self.consume(TokenType.NUMBER).value))

                unit = None
                if self.check(TokenType.UNIT):
                    unit = UnitNode(self.consume(TokenType.UNIT).value)

                name = StringNode(self.consume(TokenType.STRING).value.strip('"'))
                self.consume(TokenType.SEMICOLON)

                process.components.append(ComponentNode(quantity, unit, name))  # Changed here

            elif self.check(TokenType.STEP):
                self.consume(TokenType.STEP)
                self.consume(TokenType.COLON)
                instruction = StringNode(self.consume(TokenType.STRING).value.strip('"'))
                self.consume(TokenType.SEMICOLON)

                process.steps.append(StepNode(instruction))

            elif self.check(TokenType.TEMP):
                self.consume(TokenType.TEMP)
                self.consume(TokenType.COLON)
                temp_value = NumberNode(float(self.consume(TokenType.NUMBER).value))
                temp_unit = UnitNode(self.consume(TokenType.TEMP_UNIT).value)
                self.consume(TokenType.SEMICOLON)

                process.temperature = TemperatureNode(temp_value, temp_unit)

            else:
                # Skip unknown tokens
                self.advance()

        self.consume(TokenType.RBRACE)

        return process
```
The parser walks through the tokens, consuming them as it builds up the AST. It uses methods like consume() to match expected tokens and check() to look ahead without consuming tokens.
### AST Visualization
To better understand the structure of the parsed Process, we implement visualization using graphviz:
```python
class ASTVisualizer:

    def __init__(self):
        self.dot = graphviz.Digraph(comment='Process AST')
        self.node_count = 0

    def get_node_id(self):
        self.node_count += 1
        return f"node{self.node_count}"

    def visualize(self, node):
        self._add_node(node)
        return self.dot

    def _add_node(self, node, parent_id=None):
        if node is None:
            return None
```
The visualizer recursively traverses the AST, creating nodes and edges in the graphviz diagram to represent the hierarchical structure of the Process.
## Results
Tokens:
Token(TokenType.PROCESS, 'PROCESS')
Token(TokenType.LBRACE, '{')
Token(TokenType.TITLE, 'TITLE')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Mass Production of Sedan Model X"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.YIELD, 'YIELD')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '1000')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.TIME, 'TIME')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '30')
Token(TokenType.TIME_UNIT, 'days')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.COMPONENT, 'COMPONENT')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '1000')
Token(TokenType.STRING, '"chassis frames"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.COMPONENT, 'COMPONENT')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '2000')
Token(TokenType.STRING, '"body panels"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.COMPONENT, 'COMPONENT')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '1000')
Token(TokenType.STRING, '"engines"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.COMPONENT, 'COMPONENT')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '1000')
Token(TokenType.STRING, '"transmissions"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.COMPONENT, 'COMPONENT')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '1000')
Token(TokenType.STRING, '"wheel assemblies"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.COMPONENT, 'COMPONENT')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '5000')
Token(TokenType.STRING, '"interior modules"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.COMPONENT, 'COMPONENT')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '1000')
Token(TokenType.STRING, '"painting kits"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Design validation and prototyping"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Procure and inspect raw steel and alloys"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Stamp body panels in press shop"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Weld panels and chassis into body-in-white"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Apply corrosion protection and primer"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Bake in paint oven at 180 C for 45 minutes"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Assemble powertrain (engine, transmission)"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Install powertrain into body-in-white"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Fit interior modules and wiring harnesses"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Mount wheel assemblies and brakes"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Final quality inspection and road-testing"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.STEP, 'STEP')
Token(TokenType.COLON, ':')
Token(TokenType.STRING, '"Logistics packaging and dispatch"')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.TEMP, 'TEMP')
Token(TokenType.COLON, ':')
Token(TokenType.NUMBER, '180')
Token(TokenType.TEMP_UNIT, 'C')
Token(TokenType.SEMICOLON, ';')
Token(TokenType.RBRACE, '}')
Token(TokenType.EOF, '')

Abstract Syntax Tree:
PROCESS
  TITLE
    StringNode: Mass Production of Sedan Model X
  YIELD
    servings
      NumberNode: 1000.0
  TIME
    duration
      NumberNode: 30.0
    unit
      UnitNode: days
  Components_LIST
    COMPONENT
      quantity
        NumberNode: 1000.0
      name
        StringNode: chassis frames
    COMPONENT
      quantity
        NumberNode: 2000.0
      name
        StringNode: body panels
    COMPONENT
      quantity
        NumberNode: 1000.0
      name
        StringNode: engines
    COMPONENT
      quantity
        NumberNode: 1000.0
      name
        StringNode: transmissions
    COMPONENT
      quantity
        NumberNode: 1000.0
      name
        StringNode: wheel assemblies
    COMPONENT
      quantity
        NumberNode: 5000.0
      name
        StringNode: interior modules
    COMPONENT
      quantity
        NumberNode: 1000.0
      name
        StringNode: painting kits
  STEPS_LIST
    STEP
      instruction
        StringNode: Design validation and prototyping
    STEP
      instruction
        StringNode: Procure and inspect raw steel and alloys
    STEP
      instruction
        StringNode: Stamp body panels in press shop
    STEP
      instruction
        StringNode: Weld panels and chassis into body-in-white
    STEP
      instruction
        StringNode: Apply corrosion protection and primer
    STEP
      instruction
        StringNode: Bake in paint oven at 180 C for 45 minutes
    STEP
      instruction
        StringNode: Assemble powertrain (engine, transmission)
    STEP
      instruction
        StringNode: Install powertrain into body-in-white
    STEP
      instruction
        StringNode: Fit interior modules and wiring harnesses
    STEP
      instruction
        StringNode: Mount wheel assemblies and brakes
    STEP
      instruction
        StringNode: Final quality inspection and road-testing
    STEP
      instruction
        StringNode: Logistics packaging and dispatch
  TEMPERATURE
    value
      NumberNode: 180.0
    unit
      UnitNode: C


## Conclusion
This lab explored the implementation of a Process DSL, covering lexical analysis, parsing, AST construction, and visualization. The parser effectively transforms process descriptions into structured data, enabling applications like automated instructions or nutritional analysis.
Key takeaways include the importance of tokenization, parsing, and AST design. The project reinforced both theoretical and practical skills in language processing. Future improvements could add semantic checks, error handling, and code generation for culinary applications.