
from src.Grammar import Grammar
from src.Finite_Automata import FiniteAutomata

def main():
    #  Variant 13
    production = """
    S → aB
    B → aD
    B → bB
    D → aD
    D → bS
    B → cS
    D → c
    """

    # Set up the Grammar.
    grammar = Grammar(production)
    grammar.setStartSymbol("S")
   
    grammar.addEndSymbols("D")
    print("Parsed Grammar:")
    grammar.printGrammarSet()

    # Generate strings from the grammar.
    generated_strings = grammar.getStrings()
    print("\nGenerated strings:")
    for s in generated_strings:
        print(s)

    # Set up the Finite Automata based on the same grammar.
    automaton = FiniteAutomata(production)
    automaton.setStartSymbol("S")
    automaton.addEndSymbols("D")

    
    if generated_strings:
        test_str = list(generated_strings)[0]
    else:
        test_str = "aab"  # fallback option

    print(f"\nTesting string '{test_str}' with the finite automaton:")
    if automaton.checkStr(test_str):
        print("The string is accepted by the finite automaton!")
    else:
        print("The string is rejected by the finite automaton.")

if __name__ == "__main__":
    main()
