import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.common.enumerations import Players
from nim_game.agents.agent import Agent


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config) as file:
            js = str(json.load(file))
            self._environment = EnvironmentNim(int(js.split()[1][:-1]))
            self._agent = Agent(js.split()[3][1:-2])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """
        self._environment.change_state(player_step)
        if self.is_game_finished():
            return GameState(Players.USER, None, None)
        bot_step = self._agent.make_step(self._environment.get_state())
        self._environment.change_state(bot_step)
        if self.is_game_finished():
            return GameState(Players.BOT, None, None)
        return GameState(None, bot_step, self._environment.get_state())

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        return len(self._environment.get_state()) == self._environment.get_state().count(0)

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
