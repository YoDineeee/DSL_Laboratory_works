class ASTVisitor:
    """
    Base visitor class for AST traversal
    
    This implements the visitor pattern for traversing the AST.
    Subclasses should implement visit_NodeType methods for each node type.
    """
    
    def visit(self, node):
        """
        Visit a node by dispatching to the appropriate visit method
        
        Args:
            node: The AST node to visit
            
        Returns:
            The result of the specific visit method
        """
        return node.accept(self)
    
    def visit_default(self, node):
        """
        Default visit method for nodes that don't have a specific visit method
        
        Args:
            node: The AST node to visit
            
        Returns:
            None by default
        """
        return None
    
    def visit_ProcessNode(self, node):
        """Visit a ProcessNode"""
        if node.title:
            self.visit(node.title)
        if node.yield_node:
            self.visit(node.yield_node)
        if node.time_node:
            self.visit(node.time_node)
        for component in node.components:
            self.visit(component)
        for step in node.steps:
            self.visit(step)
        if node.temperature:
            self.visit(node.temperature)
    
    def visit_ComponentNode(self, node):
        """Visit a ComponentNode"""
        self.visit(node.quantity)
        self.visit(node.name)
        if node.unit:
            self.visit(node.unit)
    
    def visit_StepNode(self, node):
        """Visit a StepNode"""
        self.visit(node.instruction)
    
    def visit_TitleNode(self, node):
        """Visit a TitleNode"""
        self.visit(node.title)
    
    def visit_YieldNode(self, node):
        """Visit a YieldNode"""
        self.visit(node.servings)
    
    def visit_TimeNode(self, node):
        """Visit a TimeNode"""
        self.visit(node.duration)
        self.visit(node.unit)
    
    def visit_TemperatureNode(self, node):
        """Visit a TemperatureNode"""
        self.visit(node.value)
        self.visit(node.unit)
    
    def visit_StringNode(self, node):
        """Visit a StringNode"""
        pass
    
    def visit_NumberNode(self, node):
        """Visit a NumberNode"""
        pass
    
    def visit_UnitNode(self, node):
        """Visit a UnitNode"""
        pass
