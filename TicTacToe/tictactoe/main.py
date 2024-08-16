import sys

import pygame as pg
from configs.configs import Configs
from core.logic.game_logic import GameLogic
from core.screen import Screen
from game import Game


class Main:

    def __init__(self) -> None:
        self.is_running: bool = True

        self.on_init()


    def on_init(self) -> None:
        pg.init()

        self.configs = Configs()
        self.screen = Screen(self)
        self.logic = GameLogic(self)
        self.game = Game(self)


    def update(self, **kwargs) -> None:
        self.configs.update(**kwargs)
        self.screen.update()
        self.logic.update()


    def run(self) -> None:
        self.game.loop()


    def quit(self) -> None:
        if not self.is_running:
            pg.quit()
            sys.exit("TicTacToe says goodbye!")


if __name__ == "__main__":
    app = Main()
    app.run()
