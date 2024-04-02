from __future__ import annotations

class State:
    name: str
    transitions: dict[str, State]
    alphabet: list[str]

    def __init__(self, name: str, alphabet: list[str]):
        self.name = name
        self.transitions = {}
        self.alphabet = alphabet
    
    def add_transition(self, symbol: str, dest: State):
        if symbol in self.transitions:
            raise ValueError(f"Transition {symbol} already exists")
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol {symbol} not in alphabet")
        self.transitions[symbol] = dest
    
    def check(self):
        for symbol in self.alphabet:
            if symbol not in self.transitions:
                raise ValueError(f"Transition {symbol} not defined")
    
    def display(self):
        print(f"State {self.name}:")
        for symbol, dest in self.transitions.items():
            print(f"{self.name} -> {dest.name}: {symbol}")

class DFA:
    state: list[State]
    alphabet: list[str]
    start_state: State
    final_states: list[State]

    def __init__(self, alphabet: list[str]):
        self.alphabet = alphabet
        self.state = []
        self.start_state = None
        self.final_states = []
    
    def check(self):
        for s in self.state:
            s.check()
        for s in self.final_states:
            if s not in self.state:
                raise ValueError(f"Final state {s.name} not in state list")
        if self.start_state not in self.state:
            raise ValueError(f"Start state {self.start_state.name} not in state list")

    
    def add_state(self, state: State):
        self.state.append(state)
    
    def gen_state(self) -> State:
        s = State(self.alphabet)
        self.state.append(s)
        return s
    
    def run(self, input: str, verbose: bool = False) -> bool:
        current_state = self.start_state
        for idx, symbol in enumerate(input):
            dest_state = current_state.transitions[symbol]
            if verbose:
                print(f"transition {idx}: {current_state.name} -> {dest_state.name}: {symbol}")
            current_state = dest_state
        return current_state in self.final_states
    
    def display(self):
        for s in self.state:
            s.display()
        print(f"Start state: {self.start_state.name}")
        print("Final states:")
        for s in self.final_states:
            print(s.name)

