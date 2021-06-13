from typing import Optional

import messages
from game import Game, Original1P, Original2P, Mastermind44
from utils import prompt, MasterMindException


def score():
    print("=======================================")
    print("Name \t\t Score \t Games\t Average")    

class Mastermind:

    @staticmethod
    def _select_game() -> Game:
        selection: str = prompt()
        selection_lower: str = selection.lower()
        if selection_lower == 'a':
            return Original2P()
        elif selection_lower == 'b':
            return Original1P()
        elif selection_lower == 'c':
            return Mastermind44()
        raise MasterMindException(messages.INVALID_SELECTION)


    def play(self) -> None:
        print(messages.WELCOME_MESSAGE.format(my_name="YOUR NAME"))

        while True:
            print(messages.MENU)
            selection: str = prompt()
            selection_lower: str = selection.lower()
            if selection_lower == 'r':
                print("Enter Your Name")
                name = prompt()
                print("Welcome  "+str(name))
            elif selection_lower == 's':
                score()
            elif selection_lower == 'p':
                game: Optional[Game] = None
                print(messages.GAME_OPTIONS)
                while game is None:
                    try:
                        game = self._select_game()
                    except MasterMindException as e:
                        print(e)
            elif selection_lower == 'q':
                return 
        




if __name__ == "__main__":
    m = Mastermind()
    m.play()
