from src.Grammar import Grammar
from src.FiniteAutomata import FiniteAutomata

def main():
    production = """
    S → aB | c
    B → aD | bB | cC
    D → aD | bS | c
    C → c
    """

    # Test Grammar
    grammar = Grammar(production)
    grammar.setStartSymbol("S")
    grammar.addEndSymbols(["C", "D"])

    print("Parsed Grammar:")
    grammar.printGrammarSet()

    generated_strings = grammar.getStrings()
    print(f"\nGenerated strings (first {len(generated_strings)}):")
    for s in sorted(generated_strings):
        print(f"  {s}")

    # Test FiniteAutomata
    automaton = FiniteAutomata(production)
    automaton.setStartSymbol("S")
    automaton.addEndSymbols(["C", "D"])

    test_strings = ["c", "ac", "aac", "abc", "cccc", "abcc"]
    print(f"\nTesting strings with automaton:")
    for test_str in test_strings:
        result = "Accepted!" if automaton.checkStr(test_str) else "Rejected!"
        print(f"  '{test_str}': {result}")

if __name__ == "__main__":
    main()
