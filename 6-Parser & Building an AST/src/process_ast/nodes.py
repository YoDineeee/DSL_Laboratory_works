from process_ast.base import ASTNode

class ProcessNode(ASTNode):
    """Node representing the entire process"""
    
    def __init__(self):
        """Initialize a process node with empty fields"""
        self.title = None
        self.yield_node = None
        self.time_node = None
        self.components = []
        self.steps = []
        self.temperature = None
    
    def __str__(self, level=0):
        """Convert the process node to a string representation"""
        indent = "  " * level
        result = f"{indent}PROCESS\n"
        
        if self.title:
            result += self.title.__str__(level + 1)
            
        if self.yield_node:
            result += self.yield_node.__str__(level + 1)
            
        if self.time_node:
            result += self.time_node.__str__(level + 1)
            
        if self.components:
            result += f"{indent}  COMPONENTS_LIST\n"
            for component in self.components:
                result += component.__str__(level + 2)
                
        if self.steps:
            result += f"{indent}  STEPS_LIST\n"
            for step in self.steps:
                result += step.__str__(level + 2)
                
        if self.temperature:
            result += self.temperature.__str__(level + 1)
            
        return result


class ComponentNode(ASTNode):
    """Node representing a component in the process"""
    
    def __init__(self, quantity, name, unit=None):
        """
        Initialize a component node
        
        Args:
            quantity: The component quantity (NumberNode)
            name: The component name (StringNode)
            unit: Optional unit (UnitNode)
        """
        self.quantity = quantity
        self.name = name
        self.unit = unit
    
    def __str__(self, level=0):
        """Convert the component node to a string representation"""
        indent = "  " * level
        result = f"{indent}COMPONENT\n"
        result += f"{indent}  quantity\n{self.quantity.__str__(level + 2)}"
        
        if self.unit:
            result += f"{indent}  unit\n{self.unit.__str__(level + 2)}"
            
        result += f"{indent}  name\n{self.name.__str__(level + 2)}"
        
        return result


class StepNode(ASTNode):
    """Node representing a process step"""
    
    def __init__(self, instruction):
        """
        Initialize a step node
        
        Args:
            instruction: The step instruction (StringNode)
        """
        self.instruction = instruction
    
    def __str__(self, level=0):
        """Convert the step node to a string representation"""
        indent = "  " * level
        return f"{indent}STEP\n{indent}  instruction\n{self.instruction.__str__(level + 2)}"


class TitleNode(ASTNode):
    """Node representing the process title"""
    
    def __init__(self, title):
        """
        Initialize a title node
        
        Args:
            title: The process title (StringNode)
        """
        self.title = title
    
    def __str__(self, level=0):
        """Convert the title node to a string representation"""
        indent = "  " * level
        return f"{indent}TITLE\n{self.title.__str__(level + 1)}"


class YieldNode(ASTNode):
    """Node representing the process yield"""
    
    def __init__(self, servings):
        """
        Initialize a yield node
        
        Args:
            servings: The number of servings/units produced (NumberNode)
        """
        self.servings = servings
    
    def __str__(self, level=0):
        """Convert the yield node to a string representation"""
        indent = "  " * level
        return f"{indent}YIELD\n{indent}  servings\n{self.servings.__str__(level + 2)}"


class TimeNode(ASTNode):
    """Node representing the process time"""
    
    def __init__(self, duration, unit):
        """
        Initialize a time node
        
        Args:
            duration: The time duration (NumberNode)
            unit: The time unit (UnitNode)
        """
        self.duration = duration
        self.unit = unit
    
    def __str__(self, level=0):
        """Convert the time node to a string representation"""
        indent = "  " * level
        return f"{indent}TIME\n{indent}  duration\n{self.duration.__str__(level + 2)}{indent}  unit\n{self.unit.__str__(level + 2)}"


class TemperatureNode(ASTNode):
    """Node representing a temperature setting"""
    
    def __init__(self, value, unit):
        """
        Initialize a temperature node
        
        Args:
            value: The temperature value (NumberNode)
            unit: The temperature unit (UnitNode)
        """
        self.value = value
        self.unit = unit
    
    def __str__(self, level=0):
        """Convert the temperature node to a string representation"""
        indent = "  " * level
        return f"{indent}TEMPERATURE\n{indent}  value\n{self.value.__str__(level + 2)}{indent}  unit\n{self.unit.__str__(level + 2)}"
