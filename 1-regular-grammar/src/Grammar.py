
from collections import defaultdict

class Grammar:
    def __init__(self, grammar_str):
        # Parse the grammar from the given string.
        self.parsed_grammar = self.parseGrammar(grammar_str)
        self.start_symbol = None
        self.end_symbols = []  # Nonterminals that yield terminal productions.

    def setStartSymbol(self, start_symbol):
        self.start_symbol = start_symbol

    def addEndSymbols(self, end_symbol):
        if isinstance(end_symbol, list):
            self.end_symbols.extend(end_symbol)
        else:
            self.end_symbols.append(end_symbol)

    def parseGrammar(self, grammar_str):
       
        productions = defaultdict(list)
        for line in grammar_str.splitlines():
            if line.strip():
                # Expect the production to be of the form: NonTerminal → production
                non_terminal, production = line.split('→')
                nt = non_terminal.strip()
                prod = production.strip().replace(" ", "")
                if len(prod) == 1:
                    # Terminal production (e.g., D → c)
                    productions[nt].append((prod, None))
                elif len(prod) == 2:
                    # Production with a nonterminal (e.g., S → aB)
                    productions[nt].append((prod[0], prod[1]))
                else:
                    # Support for longer right-hand sides if necessary.
                    productions[nt].append((prod[0], prod[1:]))
        return productions

    def printGrammarSet(self):
        for non_terminal, productions in self.parsed_grammar.items():
            print(f"{non_terminal}: {productions}")

    def getStrings(self, max_count=5, max_depth=10):
      
        result_strs = set()

        def rec(nt, current, depth):
            if depth > max_depth:
                return
            for prod in self.parsed_grammar.get(nt, []):
                terminal, next_nt = prod
                new_str = current + terminal
                # If production is terminal (or we are at an end symbol) add the string.
                if next_nt is None or nt in self.end_symbols:
                    result_strs.add(new_str)
                    if len(result_strs) >= max_count:
                        return
                else:
                    rec(next_nt, new_str, depth + 1)
                    if len(result_strs) >= max_count:
                        return

        rec(self.start_symbol, "", 0)
        return result_strs
