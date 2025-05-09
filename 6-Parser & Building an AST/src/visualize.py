try:
    import graphviz
except ImportError:
    print("Graphviz not installed. Run: pip install graphviz")
    print("Note: You also need the Graphviz executable installed on your system.")

from process_ast.visitor import ASTVisitor

class GraphvizVisitor(ASTVisitor):
    """
    Visitor that creates a Graphviz visualization of the AST
    """
    
    def __init__(self):
        """Initialize with a new Graphviz digraph"""
        self.graph = graphviz.Digraph(comment='Process AST')
        self.node_count = 0
    
    def get_node_id(self):
        """Generate a unique node ID"""
        self.node_count += 1
        return f"node{self.node_count}"
    
    def visit_ProcessNode(self, node):
        """Visit a ProcessNode and create its visualization"""
        process_id = self.get_node_id()
        self.graph.node(process_id, 'Process')
        
        if node.title:
            title_id = self.get_node_id()
            self.graph.node(title_id, 'Title')
            self.graph.edge(process_id, title_id)
            self.visit_with_parent(node.title, title_id)
        
        if node.yield_node:
            yield_id = self.get_node_id()
            self.graph.node(yield_id, 'Yield')
            self.graph.edge(process_id, yield_id)
            self.visit_with_parent(node.yield_node, yield_id)
        
        if node.time_node:
            time_id = self.get_node_id()
            self.graph.node(time_id, 'Time')
            self.graph.edge(process_id, time_id)
            self.visit_with_parent(node.time_node, time_id)
        
        if node.components:
            components_id = self.get_node_id()
            self.graph.node(components_id, 'Components')
            self.graph.edge(process_id, components_id)
            
            for component in node.components:
                component_id = self.get_node_id()
                self.graph.node(component_id, 'Component')
                self.graph.edge(components_id, component_id)
                self.visit_with_parent(component, component_id)
        
        if node.steps:
            steps_id = self.get_node_id()
            self.graph.node(steps_id, 'Steps')
            self.graph.edge(process_id, steps_id)
            
            for step in node.steps:
                step_id = self.get_node_id()
                self.graph.node(step_id, 'Step')
                self.graph.edge(steps_id, step_id)
                self.visit_with_parent(step, step_id)
        
        if node.temperature:
            temp_id = self.get_node_id()
            self.graph.node(temp_id, 'Temperature')
            self.graph.edge(process_id, temp_id)
            self.visit_with_parent(node.temperature, temp_id)
        
        return process_id
    
    def visit_with_parent(self, node, parent_id):
        """Visit a node and connect it to its parent"""
        method_name = f"visit_{node.__class__.__name__}"
        if hasattr(self, method_name):
            node_id = getattr(self, method_name)(node)
            if node_id and parent_id:
                self.graph.edge(parent_id, node_id)
        else:
            self.visit_default_with_parent(node, parent_id)
    
    def visit_default_with_parent(self, node, parent_id):
        """Default visit method for nodes without specific handlers"""
        node_id = self.get_node_id()
        self.graph.node(node_id, str(node.__class__.__name__))
        self.graph.edge(parent_id, node_id)
        return node_id
    
    def visit_ComponentNode(self, node):
        """Visit a ComponentNode and create its visualization"""
        component_id = self.get_node_id()
        
        # Add quantity
        quantity_id = self.get_node_id()
        self.graph.node(quantity_id, 'Quantity')
        self.graph.edge(component_id, quantity_id)
        self.visit_with_parent(node.quantity, quantity_id)
        
        # Add unit if present
        if node.unit:
            unit_id = self.get_node_id()
            self.graph.node(unit_id, 'Unit')
            self.graph.edge(component_id, unit_id)
            self.visit_with_parent(node.unit, unit_id)
        
        # Add name
        name_id = self.get_node_id()
        self.graph.node(name_id, 'Name')
        self.graph.edge(component_id, name_id)
        self.visit_with_parent(node.name, name_id)
        
        return component_id
    
    def visit_StepNode(self, node):
        """Visit a StepNode and create its visualization"""
        step_id = self.get_node_id()
        
        instruction_id = self.get_node_id()
        self.graph.node(instruction_id, 'Instruction')
        self.graph.edge(step_id, instruction_id)
        self.visit_with_parent(node.instruction, instruction_id)
        
        return step_id
    
    def visit_TitleNode(self, node):
        """Visit a TitleNode and create its visualization"""
        title_id = self.get_node_id()
        self.visit_with_parent(node.title, title_id)
        return title_id
    
    def visit_YieldNode(self, node):
        """Visit a YieldNode and create its visualization"""
        yield_id = self.get_node_id()
        
        servings_id = self.get_node_id()
        self.graph.node(servings_id, 'Servings')
        self.graph.edge(yield_id, servings_id)
        self.visit_with_parent(node.servings, servings_id)
        
        return yield_id
    
    def visit_TimeNode(self, node):
        """Visit a TimeNode and create its visualization"""
        time_id = self.get_node_id()
        
        duration_id = self.get_node_id()
        self.graph.node(duration_id, 'Duration')
        self.graph.edge(time_id, duration_id)
        self.visit_with_parent(node.duration, duration_id)
        
        unit_id = self.get_node_id()
        self.graph.node(unit_id, 'Unit')
        self.graph.edge(time_id, unit_id)
        self.visit_with_parent(node.unit, unit_id)
        
        return time_id
    
    def visit_TemperatureNode(self, node):
        """Visit a TemperatureNode and create its visualization"""
        temp_id = self.get_node_id()
        
        value_id = self.get_node_id()
        self.graph.node(value_id, 'Value')
        self.graph.edge(temp_id, value_id)
        self.visit_with_parent(node.value, value_id)
        
        unit_id = self.get_node_id()
        self.graph.node(unit_id, 'Unit')
        self.graph.edge(temp_id, unit_id)
        self.visit_with_parent(node.unit, unit_id)
        
        return temp_id
    
    def visit_StringNode(self, node):
        """Visit a StringNode and create its visualization"""
        node_id = self.get_node_id()
        self.graph.node(node_id, f'String: "{node.value}"')
        return node_id
    
    def visit_NumberNode(self, node):
        """Visit a NumberNode and create its visualization"""
        node_id = self.get_node_id()
        self.graph.node(node_id, f'Number: {node.value}')
        return node_id
    
    def visit_UnitNode(self, node):
        """Visit a UnitNode and create its visualization"""
        node_id = self.get_node_id()
        self.graph.node(node_id, f'Unit: {node.value}')
        return node_id


def visualize_ast(ast, output_file='process_ast'):
    """
    Create a graphical visualization of the AST
    
    Args:
        ast: The root node of the AST
        output_file: Base filename for the output (without extension)
    
    Returns:
        The Graphviz graph object
    """
    try:
        visitor = GraphvizVisitor()
        visitor.visit(ast)
        visitor.graph.render(output_file, format='png', cleanup=True)
        print(f"AST visualization saved to {output_file}.png")
        return visitor.graph
    except Exception as e:
        print(f"Error visualizing AST: {e}")
        if "graphviz" not in str(e):
            print("Make sure you have Graphviz installed on your system.")
        return None