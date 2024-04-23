import random

def gen_test_func(test_func1, test_func2):
    def single_test(*args):
        return test_func1(*args) == test_func2(*args)
    return single_test


def random_str(alphabet: list[str]) -> str:
    return random_str_len(alphabet, 1, 10)


def random_str_len(alphabet: list[str], min_len: int, max_len: int) -> str:
    return "".join([random.choice(alphabet) for _ in range(random.randint(min_len, max_len))])


def random_str_fixed_len(alphabet: list[str], length: int) -> str:
    return "".join([random.choice(alphabet) for _ in range(length)])


def random_test(test_func, alphabet: list[str], num_tests: int, test_func2 = None, input_gen = random_str):
    for _ in range(num_tests):
        test_input = input_gen(alphabet)
        if test_func2 is not None:
            result = (test_func(test_input) == test_func2(test_input))
            if not result:
                print(test_input)
                print(test_func(test_input))
                print(test_func2(test_input))
                assert False
        else:
            res = test_func(test_input)
            if(not res):
                print("failed", test_input)
                return
