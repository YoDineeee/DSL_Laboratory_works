from grammar import Grammar
from graphviz import Digraph


class FiniteAutomaton:
    def __init__(self, states, alphabet, initial_state, final_state, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_state = final_state
        self.transitions = transitions

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

    def __get_productions(self):
        productions = {}
        for state in self.states:
            productions[state] = []

        for transition in self.transitions:
            if transition["to"] in self.final_state:
                productions[transition["state"]].append(transition["symbol"])
            else:
                productions[transition["state"]].append(transition["symbol"] + transition["to"])
        return productions

    def convert_to_grammar(self):
        non_terminals = self.states
        terminals = self.alphabet
        initial_state = self.initial_state
        productions = self.__get_productions()
        grammar = Grammar(non_terminals, terminals, productions, initial_state)
        return grammar

    def visualize(self, name):
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

        dot.render(name, format='png', view=True)

    def convert_to_dfa(self):
        if self.is_deterministic():
            return self

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

        def move(states, symbol):
            result = set()
            for state in states:
                for transition in self.transitions:
                    if transition["state"] == state and transition["symbol"] == symbol:
                        result.add(transition["to"])
            return result

        initial_dfa_state = frozenset(epsilon_closure({self.initial_state}))

        dfa_states = [initial_dfa_state]
        dfa_transitions = []
        unprocessed_states = [initial_dfa_state]

        state_mapping = {initial_dfa_state: "q0"}

        while unprocessed_states:
            current_state_set = unprocessed_states.pop(0)

            for symbol in self.alphabet:
                if symbol == "":
                    continue

                next_states = move(current_state_set, symbol)
                next_state_closure = frozenset(epsilon_closure(next_states))

                if next_state_closure and next_state_closure not in dfa_states:
                    dfa_states.append(next_state_closure)
                    unprocessed_states.append(next_state_closure)
                    state_mapping[next_state_closure] = f"q{len(state_mapping)}"

                if next_state_closure:
                    dfa_transitions.append({
                        "state": state_mapping[current_state_set],
                        "symbol": symbol,
                        "to": state_mapping[next_state_closure]
                    })

        dfa_final_states = []
        for dfa_state_set in dfa_states:
            if any(state in self.final_state for state in dfa_state_set):
                dfa_final_states.append(state_mapping[dfa_state_set])

        dfa_state_names = list(state_mapping.values())

        dfa = FiniteAutomaton(
            states=dfa_state_names,
            alphabet=[symbol for symbol in self.alphabet if symbol != ""],
            initial_state="q0",
            final_state=dfa_final_states,
            transitions=dfa_transitions
        )

        return dfa
