# test_formal_language.py
import unittest
from src.Grammar import Grammar
from src.Finite_Automata import FiniteAutomata

class TestFormalLanguage(unittest.TestCase):
    def setUp(self):
        self.production = """
        S → aB
        B → aD
        B → bB
        D → aD
        D → bS
        B → cS
        D → c
        """
        self.grammar = Grammar(self.production)
        self.grammar.setStartSymbol("S")
        self.grammar.addEndSymbols("D")
        self.automaton = FiniteAutomata(self.production)
        self.automaton.setStartSymbol("S")
        self.automaton.addEndSymbols("D")

    def test_generated_strings(self):
        strings = self.grammar.getStrings()
        self.assertTrue(len(strings) > 0, "Should generate at least one string.")

    def test_automaton_accepts_generated_string(self):
        for s in self.grammar.getStrings():
            self.assertTrue(self.automaton.checkStr(s),
                            f"The automaton should accept the string {s}")

    def test_automaton_rejects_invalid_string(self):
        self.assertFalse(self.automaton.checkStr("zzz"))
        self.assertFalse(self.automaton.checkStr("abcabc"))

if __name__ == "__main__":
    unittest.main()
