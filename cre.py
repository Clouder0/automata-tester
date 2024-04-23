from __future__ import annotations
from dataclasses import dataclass
import re

from nfa import NFA
from tester import gen_test_func, random_test


DEBUG = False

@dataclass
class symbol:
    name: str
    
@dataclass
class union:
    lhs: symbol | union | star | concat
    rhs: symbol | union | star | concat

@dataclass
class star:
    inner: symbol | union | star | concat

@dataclass
class concat:
    lhs: symbol | union | star | concat
    rhs: symbol | union | star | concat
    
def debug_print(*args):
    if DEBUG:
        print(*args)
    
def parse(pattern: str):
    debug_print(f"pattern {pattern}")
    # check symbol first
    if pattern[0] != '(':
        idx = pattern.find('(')
        if idx == -1:
            debug_print("symbol")
            return symbol(pattern)
        debug_print(f"symbol prefix concat, {pattern[:idx]} {pattern[idx:]}")
        return concat(symbol(pattern[:idx]), parse(pattern[idx:]))

    # handle concat
    bracket_num = 0
    for i, c in enumerate(pattern):
        if c == '(':
            bracket_num += 1
        elif c == ')':
            bracket_num -= 1
            if bracket_num == 0:
                # found one concat
                if i + 1 < len(pattern): 
                    debug_print(f"potential concat, {pattern[:i + 1]} {pattern[i + 1:]}")
                    if pattern[i + 1] == '*':
                        if i + 2 < len(pattern):
                            # concat with star
                            debug_print(f"concat with star, {pattern[:i + 2]} {pattern[i + 2:]}")
                            return concat(parse(pattern[:i + 2]), parse(pattern[i + 2:]))
                    else:
                        # normal concat
                        return concat(parse(pattern[:i + 1]), parse(pattern[i + 1:]))
    
    if bracket_num != 0:
        raise ValueError("Unbalanced brackets")

    # now it's single element
    # check star
    if pattern[-1] == '*':
        debug_print("star")
        return star(parse(pattern[1:-2]))
    
    # now union
    debug_print("union")
    bracket_num = 0
    for i,c in enumerate(pattern):
        if c == '(':
            bracket_num += 1
        elif c == ')':
            bracket_num -= 1
        elif c == '+' and bracket_num == 1:
            debug_print(f"union, {pattern[1:i]},{pattern[i + 1:-1]}")
            # check bracket_num == 1 to ensure it's in current level
            return union(parse(pattern[1:i]), parse(pattern[i + 1:-1]))

# res = parse("(((123)*+(456+789)))*456")
# debug_print(res)

def get_alphabet(cre: symbol | union | star | concat) -> set[str]:
    if isinstance(cre, symbol):
        return {cre.name}
    if isinstance(cre, union):
        return get_alphabet(cre.lhs) | get_alphabet(cre.rhs)
    if isinstance(cre, star):
        return get_alphabet(cre.inner)
    if isinstance(cre, concat):
        return get_alphabet(cre.lhs) | get_alphabet(cre.rhs)

def cre2nfa(cre: symbol | union | star | concat,alphabet=None) -> NFA:
    if alphabet is None:
        # parse alphabet from all symbols
        alphabet = list("".join(get_alphabet(cre)))

    n = NFA(alphabet)
    if isinstance(cre, symbol):
        s1 = n.gen_state()
        s2 = n.gen_state()
        debug_print(f"symbol {cre.name}")
        s1.add_transition(cre.name, s2)
        n.start_state = s1
        n.final_states.append(s2)
        return n
    
    if isinstance(cre, union):
        n1 = cre2nfa(cre.lhs, alphabet)
        n2 = cre2nfa(cre.rhs, alphabet)
        ns = n.gen_state()
        nf = n.gen_state()
        n.state += n1.state
        n.state += n2.state
        n.start_state = ns
        n.final_states.append(nf)
        ns.add_transitions("", [n1.start_state, n2.start_state])
        n1.final_states[0].add_transition("", nf)
        n2.final_states[0].add_transition("", nf)
        return n

    if isinstance(cre, star):
        n1 = cre2nfa(cre.inner, alphabet)
        nsf = n.gen_state()
        n.start_state = nsf
        n.final_states.append(nsf)
        n.state += n1.state
        nsf.add_transition("", n1.start_state)
        n1.final_states[0].add_transition("", nsf)
        return n
    
    if isinstance(cre, concat):
        n1 = cre2nfa(cre.lhs, alphabet)
        n2 = cre2nfa(cre.rhs, alphabet)
        n.start_state = n1.start_state
        n.final_states = n2.final_states
        n.state = n1.state + n2.state
        n1.final_states[0].add_transition("", n2.start_state)
        return n

def test_cre():
    def check1(s:str):
        return re.match(r"^1*(0|(011+))*(01*)?$", s) is not None
    my_cre = parse(r"((1)*((0+011(1)*))*0(1)*+(1)*((0+011(1)*))*)")
    my_nfa = cre2nfa(my_cre)
    # my_nfa.run("10", True)
    # return
    def check_my(s:str):
        return my_nfa.run(s)
    random_test(gen_test_func(check1, check_my), ['0', '1'], 1000)

# my_cre = parse(r"((1)*((0+011(1)*))*0(1)*+(1)*((0+011(1)*))*)")
# my_nfa = cre2nfa(my_cre)
# debug_print(my_nfa.to_mermaid())
test_cre()