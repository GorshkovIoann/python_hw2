from random import randint
from copy import deepcopy

from nim_game.common.models import NimStateChange


STONE_AMOUNT_MIN = 1        # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10       # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]       # кучки

    def __init__(self, heaps_amount: int) -> None:
        if (
            not (isinstance(heaps_amount, int))
                or heaps_amount < 2 or heaps_amount > 10
                    ):
            raise ValueError()
        self._heaps = [randint(1, 10) for x in range(heaps_amount)]

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек

        :return: копия списка с кучек
        """
        return deepcopy(self._heaps)

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния
        """
        if (
            not (isinstance(state_change.heap_id, int))
                or state_change.heap_id < 0 or state_change.heap_id >= len(self._heaps)
        ):
            raise ValueError()
        if (
            not (isinstance(state_change.decrease, int)) or state_change.decrease < 1
                or state_change.decrease > self._heaps[state_change.heap_id]
        ):
            raise ValueError()
        self._heaps[state_change.heap_id] -= state_change.decrease
