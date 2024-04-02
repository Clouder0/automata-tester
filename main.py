from tester import random_test, random_str_fixed_len, random_str_len
from dfa import DFA
from dfa import State as DFAState
from mermaid_parser import parse_mermaid

def test_hw1():
    # length >= 2 and start != end
    mermaid = """stateDiagram-v2

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
    res, d = parse_mermaid(mermaid)
    if res != "DFA":
        raise ValueError("Not a DFA")
    def test_func(input: str) -> bool:
        return len(input) >= 2 and input[0] != input[-1]
    # fixed length test cases
    random_test(d.run, d.alphabet, 1000, test_func, input_gen=lambda alphabet: random_str_fixed_len(alphabet, 4)) 
    random_test(d.run, d.alphabet, 1000, test_func)


def test_hw2():
    # all substring of length 3 at most contains one '1', at least 3 characters
    mermaid = """stateDiagram-v2
#[*] --> Q0
Q0 --> Q0: 0
Q0 --> Q1: 1
Q1 --> Q2: 0
Q2 --> Q3: 0
Q3 --> Q3: 0
Q3 --> Q1: 1
Q1 --> Qn: 1
Q2 --> Qn: 1
Qn --> Qn: 0,1
#Q0 --> [*]
#Q1 --> [*]
#Q2 --> [*]
#Q3 --> [*]"""
    res, d = parse_mermaid(mermaid)
    if res != "DFA":
        raise ValueError("Not a DFA")
    def test_func(input: str) -> bool:
        for i in range(len(input) - 2):
            if input[i:i+3].count('1') > 1:
                return False
        return True
    # at least 3 characters
    random_test(d.run, d.alphabet, 1000, test_func, input_gen=lambda a : random_str_len(a, 3, 30))

def test_hw2_2():
    # all substring of length 3 at most contains one '1', at least 1 character
    mermaid = """stateDiagram-v2
#[*] --> Q4
Q4 --> Q5: 0
Q4 --> Q6: 1
Q5 --> Q0: 0
Q5 --> Q8: 1
Q8 --> Qn: 1
Q8 --> Q2: 0
Q6 --> Q9: 0
Q6 --> Q10: 1
Q9 --> Qn: 1
Q9 --> Q0: 0
Q10 --> Qn: 0,1
Q0 --> Q0: 0
Q0 --> Q1: 1
Q1 --> Q2: 0
Q2 --> Q3: 0
Q3 --> Q3: 0
Q3 --> Q1: 1
Q1 --> Qn: 1
Q2 --> Qn: 1
Qn --> Qn: 0,1
#Q0 --> [*]
#Q1 --> [*]
#Q2 --> [*]
#Q3 --> [*]
#Q4 --> [*]
#Q5 --> [*]
#Q6 --> [*]
#Q8 --> [*]
#Q9 --> [*]
#Q10 --> [*]"""
    res, d = parse_mermaid(mermaid)
    if res != "DFA":
        raise ValueError("Not a DFA")
    def test_func(input: str) -> bool:
        for i in range(len(input) - 2):
            if input[i:i+3].count('1') > 1:
                return False
        return True
    # less than 3 characters accept
    random_test(d.run, d.alphabet, 1000, test_func, input_gen=lambda a : random_str_len(a, 1, 30))



def main():
    print("Start testing...")
    test_hw1()
    print("[hw1] done.")
    test_hw2()
    print("[hw2] done.")
    test_hw2_2()
    print("[hw2][enhanced] done.")


if __name__ == "__main__":
    main()
