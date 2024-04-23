from nfa import NFA
from tester import random_test,random_str_fixed_len,random_str_len,gen_test_func
import re
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
    res,d = parse_mermaid(mermaid)
    if res != "DFA":
        raise ValueError("Not a DFA")
    def test_func(input: str) -> bool:
        return len(input) >= 2 and input[0] != input[-1]
    # fixed length test cases
    random_test(d.run,d.alphabet,1000,test_func,input_gen=lambda alphabet: random_str_fixed_len(alphabet,4)) 
    random_test(d.run,d.alphabet,1000,test_func)


def test_hw2():
    # all substring of length 3 at most contains one '1',at least 3 characters
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
Qn --> Qn: 0|1
#Q0 --> [*]
#Q1 --> [*]
#Q2 --> [*]
#Q3 --> [*]"""
    res,d = parse_mermaid(mermaid)
    if res != "DFA":
        raise ValueError("Not a DFA")
    def test_func(input: str) -> bool:
        for i in range(len(input) - 2):
            if input[i:i+3].count('1') > 1:
                return False
        return True
    # at least 3 characters
    random_test(d.run,d.alphabet,1000,test_func,input_gen=lambda a : random_str_len(a,3,30))

def test_hw2_2():
    # all substring of length 3 at most contains one '1',at least 1 character
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
Q10 --> Qn: 0|1
Q0 --> Q0: 0
Q0 --> Q1: 1
Q1 --> Q2: 0
Q2 --> Q3: 0
Q3 --> Q3: 0
Q3 --> Q1: 1
Q1 --> Qn: 1
Q2 --> Qn: 1
Qn --> Qn: 0|1
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
    res,d = parse_mermaid(mermaid)
    if res != "DFA":
        raise ValueError("Not a DFA")
    def test_func(input: str) -> bool:
        for i in range(len(input) - 2):
            if input[i:i+3].count('1') > 1:
                return False
        return True
    # less than 3 characters accept
    random_test(gen_test_func(d.run,test_func),d.alphabet,1000,input_gen=lambda a : random_str_len(a,1,30))
    
    
def homework2():
    print("Start homework 2 testing.");

    def homework2_1():
        def check(s: str):
            return not "010" in s

        def my_ans(s: str):
            res = re.match(r"^1*(0|(011+))*(01*)?$",s)
            return res is not None
        random_test(gen_test_func(check,my_ans),['0','1'],1000)
    
    def hoemwork2_2():
        def check(s: str):
            return s[0] != s[-1]

        def my_ans(s: str):
            return re.match(r"^((0(0|1)*1)|(1(0|1)*0))$",s) is not None
        random_test(gen_test_func(check,my_ans),['0','1'],1000)
    
    def homework2_4():
        def check(s: str):
            return "ba" in s[:3] and "bb" in s[-3:]
        mermaid = """stateDiagram-v2
[*] --> Q0,Q1
Q0,Q1 --> Q1: a
Q0,Q1 --> Q1,Q2,Qq0: b
Q1 --> E: a
E --> E: a,b
Q1 --> Q2: b
Q1,Q2,Qq0 --> Q3: a
Q1,Q2,Qq0 --> Q2,Qq1: b
Q2,Qq1 --> Q3,Qq2: a
Q2,Qq1 --> E: b
Q3,Qq2 --> Q3: a
Q3,Qq2 --> Q3,Q4: b
Q2 --> Q3: a
Q2 --> E: b
Q3,Qq2 --> [*]
Q3,Q4 --> Q3: a
Q3,Q4 --> Q3,Q4,Q5,Q6: b
Q3 --> Q3: a
Q3 --> Q3,Q4: b
Q3,Q4,Q5,Q6 --> Q3,Q6: a
Q3,Q4,Q5,Q6 --> Q3,Q4,Q5,Q6: b
Q3,Q6 --> Q3: a
Q3,Q6 --> Q3,Q4: b
Q3,Q4,Q5,Q6 --> [*]
Q3,Q6 --> [*]"""
        res,d = parse_mermaid(mermaid)
        if res != "DFA":
            raise ValueError("Not a DFA")
        d: DFA
        d.check()
        # return
        random_test(gen_test_func(check,d.run),['a','b'],1000)
    
    def homework2_4_2():
        def check(s:str):
            return "ba" in s[:3] and "bb" in s[-3:]
        mermaid = """stateDiagram-v2
[*] --> Q0
Q0 --> Q1: a,b,ε
Q0 --> Qq: bba
Q1 --> Q2: ba
Q2 --> Q2: a,b
Q2 --> Q3: bb
Q3 --> Q4: a,b,ε
Qq --> [*]
Q4 --> [*]"""
        res, n = parse_mermaid(mermaid,True)
        if res != "NFA":
            raise ValueError("Not an NFA")
        random_test(gen_test_func(check, n.run), ['a', 'b'], 1000)
        
    def homework2_5():
        def check(s:str):
            for l in range(len(s)):
                if abs(s[:l].count('0') - s[:l].count('1')) > 1:
                    return False
            return s.count('0') == s.count('1')
        def my_ans(s:str):
            return re.match(r"^((01)|(10))*$", s) is not None
        random_test(gen_test_func(check,my_ans), ['0','1'], 1000)
        
    def homework2_6():
        def check(s: str):
            return s.count("aa") <= 1
        def my_ans(s:str):
            return re.match(r"^a?(b+a?)*(aa)?(b+a?)*$",s) is not None
        random_test(gen_test_func(check,my_ans), ['a','b'], 1000)
    
    print("Testing homework 2.1")
    homework2_1()
    print("Testing homework 2.1 done")
    print("Testing homework 2.2")
    hoemwork2_2()
    print("Testing homework 2.2 done")
    print("Testing homework 2.4")
    homework2_4()
    homework2_4_2()
    print("Testing homework 2.4 done")
    print("Testing homework 2.5")
    homework2_5()
    print("Testing homework 2.5 done")
    print("Testing homework 2.6")
    homework2_6()
    print("Testing homework 2.6 done")




def main():
    print("Start testing...")
    homework2()


if __name__ == "__main__":
    main()
