import os
import random
from abc import ABC, abstractmethod
from typing import Optional, List

import messages
from constants import ORIGINAL_1P_GAMERULE, ORIGINAL_2P_GAMERULE, MASTERMIND_GAMERULE
from messages import MessageBankInterface
from models import CodeBreaker, GameRule, Code, CodeMaker, ComputerCodeMaker, HumanCodeMaker, AttemptFeedback, Peg
from utils import prompt, MasterMindException, CodeParsingException


class Game(MessageBankInterface, ABC):

    def __init__(self, game_rule: GameRule) -> None:
        super().__init__()
        self._game_rule: GameRule = game_rule
        self._current_round: int = 1
        self._start_game()

    def _start_game(self):
        while self._prompt_game_start():
            self._current_round = 1
            code_maker, code_breakers = self._create_players()
            print(self._get_code_maker_guide_mssg(code_maker.get_name(), code_breakers[0].get_name()))
            final_code: Code = code_maker.make_new_final_code(self._game_rule)
            self._reveal_code(code_breakers, final_code)
            game_over = False
            print(self._get_attempt_start_mssg(code_breakers[0].get_name()))
            while not game_over:
                winner: CodeBreaker = self._prompt_breakers_guessing(code_breakers, final_code)
                game_over = winner is not None or self._current_round == self._game_rule.get_max_attempts()
                if game_over:
                    self._game_over(winner, final_code)
                self._current_round = self._current_round + 1
        print(messages.QUIT_MESSAGE)

    @abstractmethod
    def _game_over(self, winner: Optional[CodeBreaker], final_code: Code) -> None:
        pass

    @abstractmethod
    def _reveal_code(self, code_breakers: List[CodeBreaker], final_code: Code) -> None:
        pass

    @abstractmethod
    def _prompt_breakers_guessing(self, code_breakers: List[CodeBreaker], final_code: Code) -> Optional[CodeBreaker]:
        pass

    def _process_prompt_breaker_guessing(self, code_breaker: CodeBreaker, final_code: Code) -> AttemptFeedback:
        attempt_code: Optional[Code] = None
        while attempt_code is None:
            attempt_input: str = prompt()
            try:
                attempt_code = Code.parse(attempt_input, self._game_rule)
            except CodeParsingException:
                print(MessageBankInterface.get_unparsable_token_mssg(self._game_rule.get_max_code_peg(), self._game_rule.allow_blank()))
        return code_breaker.make_a_guess(attempt_code, final_code)

    def _create_code_maker(self, is_computer_code_maker: bool) -> CodeMaker:

        if is_computer_code_maker:
            return ComputerCodeMaker()
        return HumanCodeMaker(self._prompt_player_name(1))

    @staticmethod
    def _prompt_player_name(player_number: int) -> str:
        print(messages.PLAYER_NAME_PROMPT.format(player_number=player_number))
        input_name = prompt()
        print()
        return input_name

    def _create_code_breaker(self, player_number: int) -> CodeBreaker:
        return CodeBreaker(self._prompt_player_name(player_number))

    def _create_players(self) -> (CodeMaker, List[CodeBreaker]):
        is_computer_code_maker = self._game_rule.is_computer_code_maker()
        code_maker = self._create_code_maker(is_computer_code_maker)
        player_number = 1 if is_computer_code_maker else 2
        code_breakers = []
        for i in range(self._game_rule.get_max_breakers()):
            code_breakers.append(self._create_code_breaker(player_number))
            player_number = player_number + 1
        return code_maker, code_breakers

    def _prompt_game_start(self) -> bool:
        print(messages.PROMPT_PLAY_OR_QUIT)
        while True:
            action = prompt().lower()
            if action != 'p' and action != 'q':
                print(messages.INVALID_SELECTION)
                continue
            print()
            return action == 'p'


class Original(Game, ABC):

    def _get_attempt_feedback_mssg(self, current_round: int, player_name: str) -> str:
        return messages.ORIGINAL_ATTEMPT_FEEDBACK.format(current_round=current_round)

    def _game_over(self, winner: Optional[CodeBreaker], final_code: Code) -> None:
        if winner is not None:
            print(messages.CORRECT_ATTEMPT.format(who="You", attempt=self._current_round))
        else:
            print(messages.GAME_OVER.format(attempt=self._game_rule.get_max_attempts(), final_code=str(final_code)))

    def __init__(self, game_rule: GameRule) -> None:
        super().__init__(game_rule)

    def _reveal_code(self, code_breakers: List[CodeBreaker], final_code: Code) -> None:
        pass

    def _get_attempt_start_mssg(self, player_name: str = None) -> str:
        return messages.ORIGINAL_START_GUESSING.format(player_name=player_name)

    def _prompt_breakers_guessing(self, code_breakers: List[CodeBreaker], final_code: Code) -> Optional[CodeBreaker]:
        for code_breaker in code_breakers:
            print(messages.ORIGINAL_ATTEMPT.format(current_round=self._current_round))
            feedback: AttemptFeedback = self._process_prompt_breaker_guessing(code_breaker, final_code)
            print(self._get_attempt_feedback_mssg(self._current_round, code_breaker.get_name())
                  + str(feedback))
            if feedback.is_winning_state(self._game_rule.get_max_code_peg()):
                return code_breaker
        return None


class Original1P(Original):

    def __init__(self) -> None:
        super().__init__(ORIGINAL_1P_GAMERULE)

    def _get_code_maker_guide_mssg(self, code_maker_name: str = None, code_breaker_name: str = None) -> str:
        return messages.ORIGINAL_1P_CODE_MAKER_GUIDE


class Original2P(Original):

    def __init__(self) -> None:
        super().__init__(ORIGINAL_2P_GAMERULE)

    def _get_code_maker_guide_mssg(self, code_maker_name: str, code_breaker_name: str) -> str:
        if code_maker_name is None:
            raise MasterMindException("Code maker name must not be none")
        return messages.ORIGINAL_2P_CODE_MAKER_GUIDE.format(code_maker_name=code_maker_name, code_breaker_name=code_breaker_name,
                                                            max_code_length=self._game_rule.get_max_code_peg())


class Mastermind44(Game):
    def __init__(self) -> None:
        super().__init__(MASTERMIND_GAMERULE)

    def _get_code_maker_guide_mssg(self, code_maker_name: str = None, code_breaker_name: str = None) -> str:
        return messages.MASTERMIND_CODE_MAKER_GUIDE

    def _get_attempt_feedback_mssg(self, current_round: int, player_name: str) -> str:
        return messages.MASTERMIND_ATTEMPT_FEEDBACK.format(who=player_name, attempt=current_round)

    def _get_attempt_start_mssg(self, player_name: str) -> str:
        return messages.MASTERMIND_START_GUESSING

    def _game_over(self, winner: Optional[CodeBreaker], final_code: Code) -> None:
        if winner is not None:
            print(messages.CORRECT_ATTEMPT.format(who=winner.get_name(), attempt=self._current_round))
        else:
            print(messages.GAME_OVER.format(attempt=self._game_rule.get_max_attempts(), final_code=str(final_code)))

    def _reveal_code(self, code_breakers: List[CodeBreaker], final_code: Code) -> None:
        def clear_screen():
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        final_code_pegs: List[Peg] = final_code.get_pegs()
        indexes_random_able = list(range(len(final_code_pegs)))
        for code_breaker in code_breakers:
            print(messages.MASTERMIND_REVEAL_GUIDE.format(player_name=code_breaker.get_name()))
            prompt()
            index_of_indexes_random_able: int = random.randint(0, len(indexes_random_able) - 1)
            random_index_to_reveal: int = indexes_random_able[index_of_indexes_random_able]
            indexes_random_able.pop(index_of_indexes_random_able)
            revealed_peg: Peg = final_code_pegs[random_index_to_reveal]
            print(messages.MASTERMIND_REVEAL_PEG.format(position=random_index_to_reveal + 1, color=revealed_peg.value))
            print(messages.MASTERMIND_CLEAR_SCREEN)
            prompt()
            clear_screen()

    def _prompt_breakers_guessing(self, code_breakers: List[CodeBreaker], final_code: Code) -> Optional[CodeBreaker]:
        for code_breaker in code_breakers:
            print(messages.MASTERMIND_PLAYER_TURN.format(player_name=code_breaker.get_name(), current_round=self._current_round,
                                                         max_code_length=self._game_rule.get_max_code_peg()))
            feedback: AttemptFeedback = self._process_prompt_breaker_guessing(code_breaker, final_code)
            print(self._get_attempt_feedback_mssg(self._current_round, code_breaker.get_name())
                  + str(feedback) + '\n')
            if feedback.is_winning_state(self._game_rule.get_max_code_peg()):
                return code_breaker
        return None
