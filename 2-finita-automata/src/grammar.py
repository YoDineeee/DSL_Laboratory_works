class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbols = start_symbol

    def print_grammar(self):
        print("Grammar:")
        print(f"Start Symbol: {self.start_symbols}")
        print("Non-Terminals:", ", ".join(self.non_terminals))
        print("Terminals:", ", ".join(self.terminals))
        print("Productions:")
        for non_terminal, rules in self.productions.items():
            print(f"  {non_terminal} -> {' | '.join(rules)}")
