from __future__ import annotations
from collections import defaultdict

class State:
    name: str
    transitions: dict[str, list[State]]
    alphabet: list[str]

    def __init__(self, name: str, alphabet: list[str]):
        self.name = name
        self.transitions = defaultdict(list)
        self.alphabet = alphabet
    
    def add_transitions(self, symbol: str, dest: list[State]):
        symbol = symbol.replace("ε","")
        for c in symbol:  # allow delta*
            if c not in self.alphabet:
                raise ValueError(f"Symbol {symbol} not in alphabet")
        self.transitions[symbol].extend(dest)
    
    def add_transition(self, symbol: str, dest: State):
        symbol = symbol.replace("ε","")
        for c in symbol:  # allow delta*
            if c not in self.alphabet:
                raise ValueError(f"Symbol {symbol} not in alphabet")
        self.transitions[symbol].append(dest)
    
    def display(self):
        print(f"State {self.name}:")
        for symbol, dest in self.transitions.items():
            for d in dest:
                print(f"{self.name} -> {d.name}: {symbol}")

status_num = 0
class NFA:
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
        global status_num
        status_num += 1
        s = State(str(status_num), self.alphabet)
        self.state.append(s)
        return s

    def search(self, current_state: State, left_str: str, verbose: bool=False, empty_step: int=0) -> bool:
        if left_str == "":
            def check_trans():
                if "" not in current_state.transitions:
                    return False
                if empty_step > len(self.state):  # avoid infinite empty loop
                    return False
                for dest in current_state.transitions[""]:
                    if verbose:
                        print(f"{current_state.name} -> {dest.name}: ε")
                    if self.search(dest, left_str, verbose, empty_step + 1):
                        return True
                return False
            return current_state in self.final_states or check_trans()
        for symbol, dest_list in current_state.transitions.items():
            if not left_str.startswith(symbol):
                continue
            for dest in dest_list:
                if verbose:
                    print(f"{current_state.name} -> {dest.name}: {symbol}")
                if self.search(dest, left_str.removeprefix(symbol), verbose):
                    return True
        return False

    def run(self, input: str, verbose: bool = False) -> bool:
        return self.search(self.start_state, input, verbose)
    
    def display(self):
        for s in self.state:
            s.display()
        print(f"Start state: {self.start_state.name}")
        print("Final states:")
        for s in self.final_states:
            print(s.name)
    
    def to_mermaid(self):
        res = "stateDiagram-v2"
        for s in self.state:
            for symbol, dest_list in s.transitions.items():
                for dest in dest_list:
                    res += f"\n{s.name} --> {dest.name}: {symbol}"
        res += f"\n[*] --> {self.start_state.name}"
        for s in self.final_states:
            res += f"\n{s.name} --> [*]"
        return res

