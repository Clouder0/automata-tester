from collections import defaultdict
from dfa import DFA, State as DFAState
import re


test_input = """stateDiagram-v2

[*] --> Q0
Q0 --> Q1: 0
Q1 --> Q1: 0
Q1 --> Q2: 1
Q2 --> Q1: 0
Q2 --> Q2: 1

Q0 --> Q3: 1
Q3 --> Q3: 1
Q3 --> Q4: 0
Q4 --> Q3: 1
Q4 --> Q4: 0

Q2 --> [*]
Q4 --> [*]"""

# parse mermaid to generate DFA
edge_regex = re.compile(r"^#?(\w+?|\[\*\])\s*-->\s*(\w+?|\[\*\])(?::\s*(.+))?$", re.MULTILINE)
# group1: source state; group2: dest state; group3: transition symbol
def parse_mermaid(mermaid: str) -> DFA:
    # judge if one state has multiple transitions with the same symbol to judge DFA/NFA
    matches = edge_regex.findall(mermaid)
    state_map: dict[str, dict[str, list[str]]] = defaultdict(dict)
    start_states = []
    final_states = []
    all_states = set()
    alphabet = set()
    
    def add_transition(src: str, dest: str, trans: str):
        alphabet.add(trans)
        all_states.add(src)
        all_states.add(dest)
        if trans not in state_map[src]:
            state_map[src][trans] = []
        state_map[src][trans].append(dest) # support NFA

    for match in matches:
        # notice that [*] is used to indicate start/final state, with no transitions
        src = match[0]
        dest = match[1]
        trans = match[2]  # might be ""
        if src == "[*]":
            start_states.append(dest)
        elif dest == "[*]":
            final_states.append(src)
        else:
            # ignore space and split by comma
            splitted = trans.replace(" ", "").split(",")  # support multiple transitions in one line
            for x in splitted:
                add_transition(src, dest, x)
                
    is_nfa = False
    for src, trans_dict in state_map.items():
        for dest in trans_dict.values():
            if len(dest) > 1:
                is_nfa = True
                break
        if is_nfa:
            break
    
    if is_nfa:
        pass
    else:
        d = DFA(list(alphabet))
        state_map_obj: dict[str, DFAState] = {}

        for s in state_map.keys():
            state_map_obj[s] = DFAState(s, alphabet)
        
        # add transitions
        for s, trans_dict in state_map.items():
            for trans, dest_list in trans_dict.items():
                state_map_obj[s].add_transition(trans, state_map_obj[dest_list[0]])
        
        for s in state_map_obj.values():
            d.add_state(s)
        
        # set start and final states
        if len(start_states) != 1:
            raise ValueError("Only one start state is allowed")
        d.start_state = state_map_obj[start_states[0]]
        d.final_states = list(map(lambda x: state_map_obj[x], final_states))
        # d.display()
        return ("DFA", d)
