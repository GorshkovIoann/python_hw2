from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        if level != 'hard' and level != 'normal' and level != 'easy':
            raise ValueError()
        self._level = AgentLevels(level)

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        if self._level == AgentLevels.EASY:
            return self._easy_step(state_curr)

        if self._level == AgentLevels.HARD:
            return self._hard_step(state_curr)

        if self._level == AgentLevels.NORMAL:
            if randint(0, 1):
                return self._easy_step(state_curr)
            return self._hard_step(state_curr)

    def _hard_step(self,  state_curr: list[int]) -> NimStateChange:
        who_win = state_curr[0]
        for heap in range(1, len(state_curr)):
            who_win ^= state_curr[heap]
        if (who_win == 0):
            return self._easy_step(state_curr)
        for heap in range(len(state_curr)):
            if (state_curr[heap] > 0):
                for take_num in range(1, state_curr[heap] + 1):
                    state_curr[heap] -= take_num
                    how_win = state_curr[0]

                    for heapi in range(1, len(state_curr)):
                        how_win ^= state_curr[heapi]
                    if (how_win == 0):
                        state_curr[heap] += take_num
                        return NimStateChange(heap, take_num)
                    state_curr[heap] += take_num

    def _easy_step(self,  state_curr: list[int]) -> NimStateChange:
        head_id = choice([i for i in range(len(state_curr)) if state_curr[i]])
        decrease = randint(1, state_curr[head_id])

        return NimStateChange(head_id, decrease)
