class ASTNode:
    """Base class for all AST nodes"""
    
    def __str__(self, level=0):
        """
        Convert the node to a string representation with proper indentation level
        
        Args:
            level (int): The indentation level for string representation
            
        Returns:
            str: String representation of the node
        """
        raise NotImplementedError("All AST nodes must implement __str__ method")
    
    def accept(self, visitor):
        """
        Accept a visitor object for traversal
        
        Args:
            visitor: A visitor object that implements visit methods for each node type
            
        Returns:
            The result of the visitor's visit method
        """
        method_name = f"visit_{self.__class__.__name__}"
        if hasattr(visitor, method_name):
            return getattr(visitor, method_name)(self)
        else:
            return visitor.visit_default(self)
