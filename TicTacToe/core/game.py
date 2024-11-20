from typing import Any

import pygame as pg


class Game():

    def __init__(self, app) -> None:
        from main import Application

        self.app: Application = app

        self.is_game_already_won: bool = False


    def update(self, **kwargs) -> None:
        self.app.update(**kwargs)

        self.is_game_already_won = False
        self.app.logic.new_game()  # Perform a setup


    def quit(self) -> None:
        self.app.is_running = False
        self.app.quit()


    def loop(self) -> None:
        self.update()


        while self.app.is_running:
            pressed_keys = pg.key.get_pressed()
            pressed_mouse_buttons = pg.mouse.get_pressed()

            # Left Click
            if pressed_mouse_buttons[0]:
                if not self.is_game_already_won:
                    pg.time.wait(100)
                    self.app.logic.next_move(self.is_game_already_won)

                    if not self.is_game_already_won:
                        self.is_game_already_won, msg = self.app.logic.check_win_or_draw()
                        if msg is not None:
                            print(f"\n[INFO] - - -> {msg}")

            self.handle_keys(pressed_keys)
            self.handle_events()
            self.app.screen.update_display()


    def handle_keys(self, pressed_keys: Any) -> None:
        # Press key 'R' to restart the game with the current configurations
        if pressed_keys[pg.K_r]:
            self.is_game_already_won = self.app.logic.new_game()

        # Press key 'N' to start a new game with the default settings
        if pressed_keys[pg.K_n]:
            self.update()

        # Press keys '1' to '0' to start a new game with predefined custom configurations
        if pressed_keys[pg.K_1]:
            custom_configs = {"GAME": {"X_COLOR": (0, 128, 128), "O_COLOR": (255, 165, 0), "BOARD_COLOR": (70, 130, 180), "BOARD_SIZE": 3}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_2]:
            custom_configs = {"GAME": {"X_COLOR": (255, 99, 71), "O_COLOR": (60, 179, 113), "BOARD_COLOR": (100, 149, 237), "BOARD_SIZE": 3}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_3]:
            custom_configs = {"GAME": {"X_COLOR": (138, 43, 226), "O_COLOR": (255, 20, 147), "BOARD_COLOR": (135, 206, 250), "BOARD_SIZE": 3}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_4]:
            custom_configs = {"GAME": {"CONSECUTIVE_SYMBOLS_TO_WIN": 3, "BOARD_SIZE": 4}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_5]:
            custom_configs = {"GAME": {"CONSECUTIVE_SYMBOLS_TO_WIN": 3, "BOARD_SIZE": 5}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_6]:
            custom_configs = {"GAME": {"CONSECUTIVE_SYMBOLS_TO_WIN": 4, "BOARD_SIZE": 6}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_7]:
            custom_configs = {"GAME": {"CONSECUTIVE_SYMBOLS_TO_WIN": 4, "BOARD_SIZE": 7}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_8]:
            custom_configs = {"GAME": {"CONSECUTIVE_SYMBOLS_TO_WIN": 5, "BOARD_SIZE": 8}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_9]:
            custom_configs = {"GAME": {"CONSECUTIVE_SYMBOLS_TO_WIN": 5, "BOARD_SIZE": 9}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()

        if pressed_keys[pg.K_0]:
            custom_configs = {"GAME": {"CONSECUTIVE_SYMBOLS_TO_WIN": 5, "BOARD_SIZE": 10}}
            self.update(custom_configs=custom_configs)
            self.is_game_already_won = self.app.logic.new_game()


    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.VIDEORESIZE:
                self.app.screen.resize_display(event.w, event.h)
