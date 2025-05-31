# Determinism in Finite Automata. Conversion from NDFA to DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata
### Author: Mohamed Dhiaeddine Hassine , st.gr.FAF-233
### Verified by: Dumitru Crețu, University Assistant 

----

## Theoretical Background

### Deterministic and Non-deterministic Finite Automata

A **finite automaton (FA)** is a computational model with a finite set of states that processes input symbols one at a time, changing states based on defined rules.

* **DFA**: One unique transition per state and input.
* **NFA**: Multiple possible transitions for a state and input, including ε-transitions.

Both recognize **regular languages**, and every NFA can be converted into an equivalent DFA.

### Regular Grammars and Finite Automata

Regular grammars (Type 3) and finite automata are equivalent:

1. Every regular grammar can be converted to a finite automaton that recognizes the same language.
2. Every finite automaton can be converted to a regular grammar that generates the same language.

This allows seamless conversion between the two without changing the language.


### Chomsky Hierarchy

The Chomsky hierarchy, introduced by Noam Chomsky, categorizes formal grammars into four types:

1. **Type 0 (Unrestricted)**: No restrictions on production rules. These grammars generate recursively enumerable languages.
2. **Type 1 (Context-sensitive)**: Productions of the form αAβ → αγβ, where A is a non-terminal and γ is a non-empty string.
3. **Type 2 (Context-free)**: Productions of the form A → γ, where A is a non-terminal.
4. **Type 3 (Regular)**: Productions of the form A → a or A → aB, where A and B are non-terminals and a is a terminal.

Each type forms a proper subset of the previous type, with Type 3 being the most restrictive.

## Objectives

This laboratory work aims to:

1. Implement the conversion of a finite automaton to a regular grammar
2. Determine whether a given finite automaton is deterministic or non-deterministic
3. Implement conversion from NDFA to DFA
4. Represent the finite automaton graphically using external visualization tools
5. Provide a method to classify a grammar based on the Chomsky hierarchy

## Implementation Description

### FiniteAutomaton Class
The FiniteAutomaton class encapsulates the core logic for building, analyzing, and transforming a finite automaton (FA). It supports NFA to DFA conversion, grammar conversion, visualization, and determinism checking.

#### Method: `is_deterministic()`
Purpose:
Checks if the FA is deterministic (i.e., each state-symbol pair leads to at most one destination state).

Logic:

    Iterates through all transitions and tracks seen [state, symbol] pairs.

    If a duplicate pair is found, it’s non-deterministic.

Time Complexity: O(n), where n = number of transitions.

```python
def is_deterministic(self):
        is_deterministic = True
        seen = []
        for transition in self.transitions:
            key = [transition["state"], transition["symbol"]]
            if key in seen:
                is_deterministic = False
                break
            seen.append(key)
        return is_deterministic
```



#### Method: `__get_productions()`
Purpose:
Private method to generate production rules from transitions for conversion to a regular grammar.

Logic:

    For every transition:

        If destination is a final state, add A → a.

        Else, add A → aB.

Time Complexity: O(n), where n = number of transitions.

```python
def __get_productions(self):
    productions = {}
    for transition in self.transitions:
        if transition["state"] not in productions:
            productions[transition["state"]] = []

    for transition in self.transitions:
        if transition["to"] not in self.final_state:
            productions[transition["state"]].append(transition["symbol"] + transition["to"])
        else:
            productions[transition["state"]].append(transition["symbol"])
    return productions
```

#### Method: `convert_to_grammar()`
Purpose:
Converts the FA to an equivalent regular grammar.

Logic:

    Uses states as non-terminals, alphabet as terminals.

    Generates productions using __get_productions().

    Returns a Grammar object.

Time Complexity: O(n)

```python
def convert_to_grammar(self):
    non_terminals = self.states
    terminals = self.alphabet
    initial_state = self.initial_state
    productions = self.__get_productions()
    grammar = Grammar(non_terminals, terminals, productions, initial_state)
    return grammar
```
#### Method: `visualize()`

Method: visualize(name)

Purpose:
Uses Graphviz (Digraph) to render the finite automaton as a state diagram.

Logic:

    States are styled: initial state dashed, final states double-circled.

    Adds directed edges for each transition labeled with the input symbol.

    Exports a PNG image.

Time Complexity: O(n), where n = number of transitions.

```python
def visualize(self):
    dot = Digraph(comment='Finite Automaton')

    for state in self.states:
        if state == self.initial_state:
            dot.node(state, shape='doublecircle', style='dashed')
        elif state in self.final_state:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    for transition in self.transitions:
        dot.edge(transition["state"], transition["to"], label=transition["symbol"])

    dot.render('finite_automaton', format='png', view=True)
```

#### Method: `convert_to_dfa()`
Purpose:
Converts a non-deterministic FA (with or without ε-transitions) into an equivalent deterministic finite automaton (DFA).

Key Steps:

    Epsilon Closure:

        Expands a set of states to include all reachable states via ε-transitions.

    Move Function:

        Computes reachable states from a set via a specific symbol.

    Subset Construction:

        Uses sets of states (represented as frozenset) to build DFA states.

        Tracks unprocessed sets and builds a state mapping (state_mapping).

        Adds transitions for every symbol.

    Final States:

        DFA final states are those that include any original FA final state.

Output:
Returns a new FiniteAutomaton representing the DFA.

Time Complexity: O(2^n * m), where n = number of states, m = number of input symbols (due to subset construction).


```python
def convert_to_dfa(self):
    # If the automaton is already deterministic, return it as is
    if self.is_deterministic():
        return self

    # Get the epsilon closure for a set of states
    def epsilon_closure(states):
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for transition in self.transitions:
                if transition["state"] == state and transition["symbol"] == "":
                    if transition["to"] not in closure:
                        closure.add(transition["to"])
                        stack.append(transition["to"])
        return closure

    # Get the next states for a given set of states and input symbol
    def move(states, symbol):
        result = set()
        for state in states:
            for transition in self.transitions:
                if transition["state"] == state and transition["symbol"] == symbol:
                    result.add(transition["to"])
        return result

    # Start with the epsilon closure of the initial state
    initial_dfa_state = frozenset(epsilon_closure({self.initial_state}))

    # Initialize DFA states and transitions
    dfa_states = [initial_dfa_state]
    dfa_transitions = []
    unprocessed_states = [initial_dfa_state]

    # Map of DFA states (which are sets of NDFA states) to state names
    state_mapping = {initial_dfa_state: "q0"}

    # Process all unprocessed DFA states
    while unprocessed_states:
        current_state_set = unprocessed_states.pop(0)

        # For each input symbol
        for symbol in self.alphabet:
            if symbol == "":  # Skip epsilon transitions in the DFA
                continue

            # Get the next state set
            next_states = move(current_state_set, symbol)
            next_state_closure = frozenset(epsilon_closure(next_states))

            # If this is a new state, add it to the list of states to process
            if next_state_closure and next_state_closure not in dfa_states:
                dfa_states.append(next_state_closure)
                unprocessed_states.append(next_state_closure)
                state_mapping[next_state_closure] = f"q{len(state_mapping)}"

            # Add the transition if the next state set is not empty
            if next_state_closure:
                dfa_transitions.append({
                    "state": state_mapping[current_state_set],
                    "symbol": symbol,
                    "to": state_mapping[next_state_closure]
                })

    # Determine the final states of the DFA
    dfa_final_states = []
    for dfa_state_set in dfa_states:
        # If any NDFA state in this set is a final state, the DFA state is final
        if any(state in self.final_state for state in dfa_state_set):
            dfa_final_states.append(state_mapping[dfa_state_set])

    # Create list of state names for the DFA
    dfa_state_names = list(state_mapping.values())

    # Create the new DFA
    dfa = FiniteAutomaton(
        states=dfa_state_names,
        alphabet=[symbol for symbol in self.alphabet if symbol != ""],  # Remove epsilon
        initial_state="q0",
        final_state=dfa_final_states,
        transitions=dfa_transitions
    )

    return dfa
```


### Grammar Class

The `Grammar` class represents a formal grammar with the following components:
- Non-terminal symbols
- Terminal symbols
- Production rules
- Start symbol

```python
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
        print(self.productions)
```


### Results

This laboratory work successfully addressed the objectives related to finite automata and formal languages within the Chomsky hierarchy. The implementation demonstrated:

1. A comprehensive conversion of finite automata to regular grammars through the `convert_to_grammar()` method, accurately transforming states to non-terminals and transitions to production rules.

2. A reliable determinism checker through the `is_deterministic()` method, which correctly identified when multiple transitions exist for the same state-input pair.

3. The visualization capability provided through Graphviz integration offered a clear graphical representation of finite automata with appropriate notations for initial, final, and regular states.


Through this work, the fundamental theoretical concepts of formal languages—particularly the relationship between finite automata and regular grammars—were effectively demonstrated in practice, providing a solid foundation for understanding more complex language processing systems.