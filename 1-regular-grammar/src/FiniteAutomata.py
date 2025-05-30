from collections import defaultdict

class FiniteAutomata:
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

    def checkStr(self, check_str):
        def rec(nt, i):
            if i == len(check_str):
                return self._canDeriveEpsilon(nt)

            for prod in self.parsed_grammar.get(nt, []):
                terminal, next_nt = prod

                if i < len(check_str) and check_str[i] == terminal:
                    if next_nt is None:
                        if i + 1 == len(check_str):
                            return True
                    else:
                        if rec(next_nt, i + 1):
                            return True
            return False

        if not self.start_symbol:
            return False
        return rec(self.start_symbol, 0)

    def _canDeriveEpsilon(self, nt):
        return False
