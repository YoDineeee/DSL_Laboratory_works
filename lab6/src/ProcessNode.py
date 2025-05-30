class ProcessNode:
    def __init__(self):
        self.title = None
        self.yield_node = None
        self.time_node = None
        self.components = []  # Initialize as empty list
        self.steps = []       # Initialize as empty list
        self.temperature = None

    def __str__(self, level=0):
        indent = "  " * level
        result = f"{indent}PROCESS\n"

        if self.title:
            result += self.title.__str__(level + 1)

        if self.yield_node:
            result += self.yield_node.__str__(level + 1)

        if self.time_node:
            result += self.time_node.__str__(level + 1)

        if self.components:  # <-- Fixed here
            result += f"{indent}  Components_LIST\n"
            for component in self.components:
                result += component.__str__(level + 2)

        if self.steps:
            result += f"{indent}  STEPS_LIST\n"
            for step in self.steps:
                result += step.__str__(level + 2)

        if self.temperature:
            result += self.temperature.__str__(level + 1)

        return result
