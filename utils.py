from typing import List
import random

def prompt() -> str:
    return input('> ')


def convert_input_to_code_values(input_code: str) -> List[str]:
    return [char for char in input_code]

def score(names):
    print("=======================================")
    print("Name \t\t Score \t Games\t Average")
    for name in names:
        print(name +"\t\t "+str(random.randint(10,100))+"\t "+
        str(random.randint(1,10))+"\t "+ str(random.randint(20,100)))
    print("=======================================")        


class MasterMindException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CodeParsingException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
