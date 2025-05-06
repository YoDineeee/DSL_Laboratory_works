from finite_automata import FiniteAutomaton

def main():
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b"}
    transitions = [
        {"state": "q0", "symbol": "a", "to": "q0"},
        {"state": "q0", "symbol": "b", "to": "q1"},
        {"state": "q1", "symbol": "a", "to": "q1"},
        {"state": "q1", "symbol": "a", "to": "q2"},
        {"state": "q1", "symbol": "b", "to": "q3"},
        {"state": "q2", "symbol": "a", "to": "q2"},
        {"state": "q2", "symbol": "b", "to": "q3"}
    ]
    initial_state = "q0"
    final_state = {"q3"}

    finite_automaton = FiniteAutomaton(states, alphabet, initial_state, final_state, transitions)

    print("Is deterministic:", finite_automaton.is_deterministic())

    grammar = finite_automaton.convert_to_grammar()
    print("\nGrammar from NDFA:")
    grammar.print_grammar()

    print("\nGenerating NDFA visualization...")
    finite_automaton.visualize("NDFA_Variant13")

    print("\nConverting NDFA to DFA...")
    dfa = finite_automaton.convert_to_dfa()
    
    print("Is DFA deterministic:", dfa.is_deterministic())
    
    dfa_grammar = dfa.convert_to_grammar()
    print("\nGrammar from DFA:")
    dfa_grammar.print_grammar()
    
    print("\nGenerating DFA visualization...")
    dfa.visualize("DFA_Variant13")
    
    print("\nProcess completed successfully!")

if __name__ == "__main__":
    main()
