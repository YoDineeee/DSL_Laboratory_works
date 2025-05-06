from itertools import chain, combinations

class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
        self.N_lambda = set()

    def print_grammar(self, message="Current grammar:"):
        print(f"\n{message}")
        print(f"Non-terminals: {self.non_terminals}")
        print(f"Terminals: {self.terminals}")
        print(f"Start symbol: {self.start_symbol}")
        print("Productions:")
        for nt, prods in self.productions.items():
            print(f"  {nt} -> {' | '.join(prods)}")
        print()

    def eliminate_empty_productions(self):
        print("\nStep 1: Eliminating epsilon productions")
        
        N_lambda = set()
        
        for nt, prods in self.productions.items():
            if "ε" in prods or "epsilon" in prods:
                N_lambda.add(nt)
        
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt in N_lambda:
                    continue
                
                for prod in prods:
                    if all(symbol in N_lambda for symbol in prod):
                        N_lambda.add(nt)
                        changed = True
                        break
        
        self.N_lambda = N_lambda
        print(f"Nullable non-terminals: {N_lambda}")
        
        new_productions = {nt: [] for nt in self.productions}
        
        for nt, prods in self.productions.items():
            for prod in prods:
                if prod == "ε" or prod == "epsilon":
                    continue
                
                nullable_positions = []
                for i, symbol in enumerate(prod):
                    if symbol in N_lambda:
                        nullable_positions.append(i)
                
                all_subsets = chain.from_iterable(
                    combinations(nullable_positions, r) 
                    for r in range(len(nullable_positions) + 1)
                )
                
                for subset in all_subsets:
                    new_prod = "".join(symbol for i, symbol in enumerate(prod) if i not in subset)
                    
                    if new_prod and new_prod not in new_productions[nt]:
                        new_productions[nt].append(new_prod)
        
        self.productions = new_productions
        
        self.productions = {nt: prods for nt, prods in self.productions.items() if prods}
        
        self.print_grammar("Grammar after eliminating epsilon productions:")
        return self

    def eliminate_unit_productions(self):
        print("\nStep 2: Eliminating unit productions (renaming)")
        
        unit_pairs = {nt: {nt} for nt in self.non_terminals}
        
        changed = True
        while changed:
            changed = False
            for A in self.non_terminals:
                for prod in self.productions.get(A, []):
                    if prod in self.non_terminals:
                        B = prod
                        for C in unit_pairs.get(B, set()):
                            if C not in unit_pairs[A]:
                                unit_pairs[A].add(C)
                                changed = True
        
        print("Unit pairs:", unit_pairs)
        
        new_productions = {nt: [] for nt in self.non_terminals}
        
        for A in self.non_terminals:
            for B in unit_pairs[A]:
                for prod in self.productions.get(B, []):
                    if prod not in self.non_terminals and prod not in new_productions[A]:
                        new_productions[A].append(prod)
        
        self.productions = new_productions
        
        self.productions = {nt: prods for nt, prods in self.productions.items() if prods}
        
        self.print_grammar("Grammar after eliminating unit productions:")
        return self

    def eliminate_inaccessible_symbols(self):
        print("\nStep 3: Eliminating inaccessible symbols")
        
        accessible = {self.start_symbol}
        queue = [self.start_symbol]
        
        while queue:
            current = queue.pop(0)
            for prod in self.productions.get(current, []):
                for symbol in prod:
                    if symbol in self.non_terminals and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)
        
        print(f"Accessible non-terminals: {accessible}")
        
        inaccessible = self.non_terminals - accessible
        print(f"Inaccessible non-terminals being removed: {inaccessible}")
        
        self.non_terminals = accessible
        self.productions = {nt: prods for nt, prods in self.productions.items() if nt in accessible}
        
        self.print_grammar("Grammar after eliminating inaccessible symbols:")
        return self

    def eliminate_non_productive_symbols(self):
        print("\nStep 4: Eliminating non-productive symbols")
        
        productive = set()
        
        for nt, prods in self.productions.items():
            for prod in prods:
                if all(symbol in self.terminals for symbol in prod):
                    productive.add(nt)
                    break
        
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt in productive:
                    continue
                
                for prod in prods:
                    if all(symbol in self.terminals or symbol in productive for symbol in prod):
                        productive.add(nt)
                        changed = True
                        break
        
        print(f"Productive non-terminals: {productive}")
        
        non_productive = self.non_terminals - productive
        print(f"Non-productive non-terminals being removed: {non_productive}")
        
        self.non_terminals = productive
        
        new_productions = {}
        for nt in productive:
            new_productions[nt] = []
            for prod in self.productions.get(nt, []):
                if all(symbol not in self.non_terminals or symbol in productive for symbol in prod):
                    new_productions[nt].append(prod)
        
        self.productions = new_productions
        
        self.productions = {nt: prods for nt, prods in self.productions.items() if prods}
        
        self.print_grammar("Grammar after eliminating non-productive symbols:")
        return self

    def convert_to_binary_form(self):
        print("\nConverting productions to binary form")
        
        new_productions = {}
        new_non_terminals = set(self.non_terminals)
        next_nt_index = 1
        
        for nt, prods in self.productions.items():
            new_productions[nt] = []
            
            for prod in prods:
                if len(prod) <= 2:
                    new_productions[nt].append(prod)
                else:
                    symbols = list(prod)
                    current_nt = nt
                    
                    while len(symbols) > 2:
                        first = symbols.pop(0)
                        
                        new_nt = f"X{next_nt_index}"
                        next_nt_index += 1
                        new_non_terminals.add(new_nt)
                        
                        new_productions[current_nt] = new_productions.get(current_nt, []) + [first + new_nt]
                        current_nt = new_nt
                    
                    new_productions[current_nt] = new_productions.get(current_nt, []) + ["".join(symbols)]
        
        self.non_terminals = new_non_terminals
        self.productions = new_productions
        
        self.print_grammar("Grammar after converting to binary form:")
        return self

    def convert_terminal_mixed_productions(self):
        print("\nConverting terminal-mixed productions")
        
        new_productions = {}
        new_non_terminals = set(self.non_terminals)
        terminal_non_terminals = {}
        
        for terminal in self.terminals:
            new_nt = f"T_{terminal}"
            terminal_non_terminals[terminal] = new_nt
            new_non_terminals.add(new_nt)
            new_productions[new_nt] = [terminal]
        
        for nt, prods in self.productions.items():
            new_productions[nt] = new_productions.get(nt, [])
            
            for prod in prods:
                if len(prod) == 1:
                    new_productions[nt].append(prod)
                else:
                    new_prod = ""
                    for symbol in prod:
                        if symbol in self.terminals:
                            new_prod += terminal_non_terminals[symbol]
                        else:
                            new_prod += symbol
                    new_productions[nt].append(new_prod)
        
        self.non_terminals = new_non_terminals
        self.productions = new_productions
        
        self.print_grammar("Grammar after converting terminal-mixed productions:")
        return self

    def convert_to_chomsky_normal_form(self):
        print("\nConverting grammar to Chomsky Normal Form")
        
        self.eliminate_empty_productions()
        self.eliminate_unit_productions()
        self.eliminate_inaccessible_symbols()
        self.eliminate_non_productive_symbols()
        self.convert_to_binary_form()
        self.convert_terminal_mixed_productions()
        
        print("\nConversion to Chomsky Normal Form complete!")
        return self