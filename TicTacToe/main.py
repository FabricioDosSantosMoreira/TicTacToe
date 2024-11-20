import pygame as pg

from core import Game, Screen
from core.configs import GameConfigs
from core.logic import GameLogic


class Application():

    def __init__(self) -> None:
        self.is_running: bool = True

        self.on_init()


    def on_init(self) -> None:
        pg.init()

        self.configs = GameConfigs()
        self.logic = GameLogic(self)

        self.screen = Screen(self)
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
        
            quit("\nBye Bye from TicTacToe v1.0.0!")


if __name__ == "__main__":
    app = Application()
    app.run()
