import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import pygame as pg


class GameConfigs():

    def __init__(self) -> None:

        self.ROOT_PATH: Path = Path(__file__).resolve().parent.parent.parent
        self.CONFIGS_PATH: Path = Path(self.ROOT_PATH / "configs.json").resolve()

        if not self.CONFIGS_PATH.exists():
            raise FileNotFoundError(
                f"\n\n\tConfig file wasn't found at: \n\n\t\t{str(self.CONFIGS_PATH)}"
            )

        self.configs: Dict[str, Any] = {}

        self.update()


    def update(self, custom_configs: Optional[Dict[str, Any]] = None) -> None:
        self.configs = self.load_configs()

        if custom_configs:
            self.merge_configs(custom_configs)


        # Screen configs
        self.SCREEN_WIDTH: int = self.get_configs("SCREEN", "WIDTH")
        self.SCREEN_HEIGHT: int = self.get_configs("SCREEN", "HEIGHT")

        if self.SCREEN_WIDTH > self.SCREEN_HEIGHT:
            self.SCREEN_WIDTH = 1280
            self.SCREEN_HEIGHT = 720

        # Define how much 'out_layer_background' should occupy. Default = 0.10 (10%)
        self.OFFSET: float = self.get_configs("SCREEN", "OFFSET")

        # Board configs
        self.BOARD_SIZE: int = self.get_configs("GAME", "BOARD_SIZE")
        self.BOARD_COLOR: Tuple[int] = self.get_configs("GAME", "BOARD_COLOR")
        self.BOARD_THICKNESS: int = self.get_configs("GAME", "BOARD_THICKNESS")
        self.WIN_LINE_THICKNESS: int = self.get_configs("GAME", "WIN_LINE_THICKNESS")
        self.WIN_LINE_COLOR: Tuple[int] = self.get_configs("GAME", "WIN_LINE_COLOR")


        # Symbols configs
        self.START_SYMBOL: str = self.get_configs("GAME", "START_SYMBOL")
        self.CONSECUTIVE_SYMBOLS_TO_WIN: int = self.get_configs("GAME", "CONSECUTIVE_SYMBOLS_TO_WIN")

        self.X_COLOR: Tuple[int] = self.get_configs("GAME", "X_COLOR")
        self.X_THICKNESS: int = self.get_configs("GAME", "X_THICKNESS")
        # Increases or decreases the size of "X" symbol, default = 0.0
        self.X_OFFSET: int = self.get_configs("GAME", "X_OFFSET")

        self.O_COLOR: Tuple[int] = self.get_configs("GAME", "O_COLOR")
        self.O_THICKNESS: int = self.get_configs("GAME", "O_THICKNESS")
        # Increases or decreases the size of "O" symbol, default = 0.0
        self.O_OFFSET: int = self.get_configs("GAME", "O_OFFSET")


        # Display configs
        self.CAPTION: str = self.get_configs("UTIL", "CAPTION")


        # Backgrounds configs
        self.BOARD_BACKGROUND: pg.Surface = pg.image.load(self.ROOT_PATH / self.get_configs("UTIL", "BOARD_BACKGROUND_PATH"))
        self.OUT_LAYER_BACKGROUND: pg.Surface = pg.image.load(self.ROOT_PATH / self.get_configs("UTIL", "OUT_LAYER_BACKGROUND_PATH"))


    def load_configs(self) -> Dict[str, Any]:
        _configs: Dict[str, Any] = {}

        try:
            with open(self.CONFIGS_PATH, mode="r", encoding="utf-8") as configs_file:
                _configs = json.load(configs_file)
        except Exception as exc:
            raise ValueError(f"\n\n\tValueError - - -> ['configs'] weren't loaded. \n\n\t\t{exc}\n")

        return _configs


    def merge_configs(self, custom_configs: Dict[str, Any]) -> None:

        def merge(d1: Dict[str, Any], d2: Dict[str, Any]) -> Any:
            for key, value in d2.items():
                if isinstance(value, dict):
                    d1[key] = merge(d1.get(key, {}), value)
                else:
                    d1[key] = value

            return d1

        self.configs = merge(self.configs, custom_configs)


    def get_configs(self, key: str, nested_key: Optional[str] = None) -> Union[Dict[str, Any], Any]:
        
        return self.configs.get(key, {}).get(nested_key, None)
