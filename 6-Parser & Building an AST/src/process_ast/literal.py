from process_ast.base import ASTNode

class LiteralNode(ASTNode):
    """Base class for all literal value nodes"""
    
    def __init__(self, value):
        """
        Initialize a literal node with a value
        
        Args:
            value: The literal value
        """
        self.value = value
    
    def __str__(self, level=0):
        """
        Convert the literal node to a string representation
        
        Args:
            level (int): The indentation level
            
        Returns:
            str: String representation of the literal value
        """
        indent = "  " * level
        return f"{indent}{self.value}\n"


class StringNode(LiteralNode):
    """Node representing a string literal"""
    pass


class NumberNode(LiteralNode):
    """Node representing a numeric literal"""
    pass


class UnitNode(LiteralNode):
    """Node representing a unit (g, ml, etc.)"""
    pass
