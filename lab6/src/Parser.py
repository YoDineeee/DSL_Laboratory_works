from NumberNode import NumberNode
from ProcessNode import ProcessNode
from StepNode import StepNode
from StringNode import StringNode
from TemperatureNode import TemperatureNode
from TimeNode import TimeNode
from TitleNode import TitleNode
from TokenType import TokenType
from UnitNode import UnitNode
from YeildNode import YieldNode
from ComponentNode import ComponentNode  # <- Added import

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.parse_process()

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

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def consume(self, token_type):
        if self.check(token_type):
            return self.advance()

        raise SyntaxError(f"Expected {token_type} but got {self.peek().token_type}")

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def is_at_end(self):
        return self.peek().token_type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]
