from Grammar import Grammar

def main():
    non_terminals = {"S", "A", "B", "C", "D"}
    terminals = {"a", "b"}
    productions = {
        "S": ["aB", "DA"],
        "A": ["a", "BD", "bDAB"],
        "B": ["b", "BA"],
        "D": ["ε", "BA"],
        "C": ["BA"]
    }
    start_symbol = "S"
    
    grammar = Grammar(non_terminals, terminals, productions, start_symbol)
    grammar.print_grammar("Initial grammar for Variant 13:")
    
    grammar.convert_to_chomsky_normal_form()


if __name__ == "__main__":
    main()