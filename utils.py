from typing import List


def prompt() -> str:
    return input('> ')


def convert_input_to_code_values(input_code: str) -> List[str]:
    return [char for char in input_code]


class MasterMindException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CodeParsingException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
