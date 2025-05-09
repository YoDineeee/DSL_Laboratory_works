from tokens import TokenType
from process_ast.nodes import (
    ProcessNode, ComponentNode, StepNode, TitleNode, 
    YieldNode, TimeNode, TemperatureNode
)
from process_ast.literal import StringNode, NumberNode, UnitNode

class Parser:
    """
    Parser for the process description language
    
    Parses tokens into an AST structure
    """
    
    def __init__(self, tokens):
        """
        Initialize the parser with a list of tokens
        
        Args:
            tokens: List of Token objects from the Lexer
        """
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        """
        Parse the tokens into an AST
        
        Returns:
            The root ProcessNode of the AST
        """
        return self.parse_process()
    
    def parse_process(self):
        """
        Parse a PROCESS block
        
        Returns:
            A ProcessNode with all its contents
        """
        # Expect PROCESS keyword
        self.consume(TokenType.PROCESS)
        # Expect opening brace
        self.consume(TokenType.LBRACE)
        
        process = ProcessNode()
        
        # Parse contents until closing brace
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            if self.match(TokenType.TITLE):
                self.consume(TokenType.COLON)
                title = self.consume(TokenType.STRING).value.strip('"')
                self.consume(TokenType.SEMICOLON)
                process.title = TitleNode(StringNode(title))
                
            elif self.match(TokenType.YIELD):
                self.consume(TokenType.COLON)
                value = float(self.consume(TokenType.NUMBER).value)
                self.consume(TokenType.SEMICOLON)
                process.yield_node = YieldNode(NumberNode(value))
                
            elif self.match(TokenType.TIME):
                self.consume(TokenType.COLON)
                value = float(self.consume(TokenType.NUMBER).value)
                unit = self.consume(TokenType.TIME_UNIT).value
                self.consume(TokenType.SEMICOLON)
                process.time_node = TimeNode(NumberNode(value), UnitNode(unit))
                
            elif self.match(TokenType.COMPONENT):
                self.consume(TokenType.COLON)
                quantity = NumberNode(float(self.consume(TokenType.NUMBER).value))
                unit = None
                if self.check(TokenType.UNIT):
                    unit = UnitNode(self.consume(TokenType.UNIT).value)
                name = StringNode(self.consume(TokenType.STRING).value.strip('"'))
                self.consume(TokenType.SEMICOLON)
                process.components.append(ComponentNode(quantity, name, unit))
                
            elif self.match(TokenType.STEP):
                self.consume(TokenType.COLON)
                instruction = StringNode(self.consume(TokenType.STRING).value.strip('"'))
                self.consume(TokenType.SEMICOLON)
                process.steps.append(StepNode(instruction))
                
            elif self.match(TokenType.TEMP):
                self.consume(TokenType.COLON)
                value = NumberNode(float(self.consume(TokenType.NUMBER).value))
                unit = UnitNode(self.consume(TokenType.TEMP_UNIT).value)
                self.consume(TokenType.SEMICOLON)
                process.temperature = TemperatureNode(value, unit)
                
            else:
                # Skip unexpected tokens
                self.advance()
        
        # Expect closing brace
        self.consume(TokenType.RBRACE)
        return process
    
    def match(self, type):
        """
        Check if current token matches the given type, and advance if it does
        
        Args:
            type: The TokenType to match
            
        Returns:
            bool: True if the token was matched and consumed
        """
        if self.check(type):
            self.advance()
            return True
        return False
    
    def check(self, type):
        """
        Check if current token is of the given type
        
        Args:
            type: The TokenType to check
            
        Returns:
            bool: True if current token matches the type
        """
        if self.is_at_end():
            return False
        return self.peek().token_type == type
    
    def advance(self):
        """
        Advance to the next token
        
        Returns:
            The previous token
        """
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def consume(self, type):
        """
        Consume the current token if it matches the expected type
        
        Args:
            type: The expected TokenType
            
        Returns:
            The consumed token
            
        Raises:
            SyntaxError: If the current token doesn't match the expected type
        """
        if self.check(type):
            return self.advance()
        
        token = self.peek()
        raise SyntaxError(f"Expected {type}, got {token.token_type} at line {token.line}, column {token.column}")
    
    def peek(self):
        """
        Look at the current token without consuming it
        
        Returns:
            The current token
        """
        return self.tokens[self.current]
    
    def previous(self):
        """
        Get the previously consumed token
        
        Returns:
            The previously consumed token
        """
        return self.tokens[self.current - 1]
    
    def is_at_end(self):
        """
        Check if we've reached the end of the token stream
        
        Returns:
            bool: True if we're at EOF
        """
        return self.peek().token_type == TokenType.EOF
