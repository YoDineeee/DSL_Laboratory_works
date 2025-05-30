from collections import defaultdict

class Grammar:
    def __init__(self, grammar_str):
        self.parsed_grammar = self.parseGrammar(grammar_str)
        self.start_symbol = None
        self.end_symbols = []

    def setStartSymbol(self, start_symbol):
        self.start_symbol = start_symbol

    def addEndSymbols(self, end_symbol):
        if isinstance(end_symbol, list):
            self.end_symbols.extend(end_symbol)
        else:
            self.end_symbols.append(end_symbol)

    def parseGrammar(self, grammar_str):
        productions = defaultdict(list)
        for line in grammar_str.strip().splitlines():
            if line.strip() and '→' in line:
                non_terminal, productions_str = line.split('→')
                nt = non_terminal.strip()
                prod_list = [p.strip() for p in productions_str.split('|')]

                for prod in prod_list:
                    prod = prod.replace(" ", "")
                    if len(prod) == 1:
                        productions[nt].append((prod, None))
                    elif len(prod) == 2:
                        productions[nt].append((prod[0], prod[1]))
                    else:
                        productions[nt].append((prod[0], prod[1:]))
        return productions

    def printGrammarSet(self):
        for non_terminal, productions in self.parsed_grammar.items():
            print(f"{non_terminal}: {productions}")

    def getStrings(self, max_count=10, max_depth=10):
        result_strs = set()

        def rec(nt, current, depth):
            if depth > max_depth or len(result_strs) >= max_count:
                return

            for prod in self.parsed_grammar.get(nt, []):
                terminal, next_nt = prod
                new_str = current + terminal

                if next_nt is None:
                    result_strs.add(new_str)
                    if len(result_strs) >= max_count:
                        return
                else:
                    rec(next_nt, new_str, depth + 1)

        if self.start_symbol:
            rec(self.start_symbol, "", 0)
        return list(result_strs)
