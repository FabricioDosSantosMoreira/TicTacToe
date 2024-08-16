from typing import Tuple

import pygame as pg
from configs.configs import Configs


class Screen:

    def __init__(self, app) -> None:
        from main import Main

        self.app: Main = app

        pg.display.init()
        pg.display.set_caption(self.app.configs.CAPTION)

        self.update()


    def update(self) -> None:
        configs: Configs = self.app.configs

        self.screen_width = configs.SCREEN_WIDTH
        self.screen_height = configs.SCREEN_HEIGHT

        self.board_background = configs.BOARD_BACKGROUND
        self.out_layer_background = configs.OUT_LAYER_BACKGROUND

        self.x_color = configs.X_COLOR
        self.x_offset = configs.X_OFFSET
        self.x_thickness = configs.X_THICKNESS

        self.o_color = configs.O_COLOR
        self.o_offset = configs.O_OFFSET
        self.o_thickness = configs.O_THICKNESS

        self.board_color = configs.BOARD_COLOR
        self.board_thickness = configs.BOARD_THICKNESS
        self.board_width = configs.BOARD_WIDTH
        self.board_height = configs.BOARD_HEIGHT

        self.top_offset = configs.TOP_OFFSET
        self.right_offset = configs.RIGHT_OFFSET

        self.win_line_color = configs.WIN_LINE_COLOR
        self.win_line_thickness = configs.WIN_LINE_THICKNESS

        self.display: pg.Surface = pg.display.set_mode((self.screen_width, self.screen_height))


    def display_update(self) -> None:
        pg.display.update()
        pg.display.flip()


    def display_blit(self) -> None:
        self.display.blit(self.out_layer_background, (0, 0))
        self.display.blit(self.board_background, (-self.right_offset, self.top_offset))


    def draw_symbol(self, row, col, board_size, symbol) -> None:
        if symbol == "X":
            self.draw_symbol_x(row, col, board_size)
        elif symbol == "O":
            self.draw_symbol_o(row, col, board_size)


    def draw_symbol_x(self, row: int, col: int, board_size: int) -> None:
        start_x_pos = ((self.board_width / (board_size * 3)) * (col * 3 + 1)) - self.x_offset
        start_y_pos = ((self.board_height / (board_size * 3)) * (row * 3 + 1)) + self.top_offset - self.x_offset
        end_x_pos = ((self.board_width / (board_size * 3)) * (col * 3 + 2)) + self.x_offset
        end_y_pos = ((self.board_height / (board_size * 3)) * (row * 3 + 2)) + self.top_offset + self.x_offset

        pg.draw.line(
            surface=self.display,
            color=self.x_color,
            start_pos=(start_x_pos, start_y_pos),
            end_pos=(end_x_pos, end_y_pos),
            width=self.x_thickness,
        )

        pg.draw.line(
            surface=self.display,
            color=self.x_color,
            start_pos=(start_x_pos, end_y_pos),
            end_pos=(end_x_pos, start_y_pos),
            width=self.x_thickness,
        )


    def draw_symbol_o(self, row: int, col: int, board_size: int) -> None:
        smaller_board_dimension = min(self.board_width, self.board_height)
        radius = (smaller_board_dimension / (board_size * 3 + board_size)) + self.o_offset

        x_center = (col + 0.5) * (self.board_width / board_size)
        y_center = ((row + 0.5) * (self.board_height / board_size)) + self.top_offset

        pg.draw.circle(surface=self.display, color=self.o_color, center=(x_center, y_center), radius=radius, width=self.o_thickness)


    def get_mouse_pos(self, board_size: int) -> Tuple[int, int]:
        x, y = pg.mouse.get_pos()
        row, col = -1, -1

        if (x < 0) | (x > self.board_width) | (y > self.board_height + self.top_offset) | (y < (self.top_offset)):
            pass
        else:
            col = int(x / (self.board_width / board_size))
            row = int((y - self.top_offset) / (self.board_height / board_size))

            if col >= board_size:
                col = col - 1
            elif row >= board_size:
                row = row - 1

        return (row, col)


    def draw_tictactoe_board(self, board_size: int) -> None:
        cell_width = self.board_width / board_size
        cell_height = self.board_height / board_size

        for i in range(1, board_size):

            # Horizontal line
            start_x_pos = 0
            end_x_pos = self.board_width - 1
            start_y_pos = cell_height * i + self.top_offset
            end_y_pos = start_y_pos

            pg.draw.line(
                surface=self.display,
                color=self.board_color,
                start_pos=(start_x_pos, start_y_pos),
                end_pos=(end_x_pos, end_y_pos),
                width=self.board_thickness,
            )

            # Vertical line
            start_x_pos = cell_width * i
            end_x_pos = start_x_pos
            start_y_pos = 0 + self.top_offset
            end_y_pos = self.board_height + self.top_offset

            pg.draw.line(
                surface=self.display,
                color=self.board_color,
                start_pos=(start_x_pos, start_y_pos),
                end_pos=(end_x_pos, end_y_pos),
                width=self.board_thickness,
            )


    def get_cell_midpoint(self, board_size: int) -> Tuple[float, float]:
        cell_width_center = ((self.board_width) / board_size) / 2
        cell_height_center = ((self.board_height) / board_size) / 2

        return (cell_width_center, cell_height_center)


    def draw_horizontal_win_line(self, start_row: int, start_col: int, board_size: int, total_occurrences: int) -> None:
        cell_width_center, cell_height_center = self.get_cell_midpoint(board_size)

        start_x_pos = cell_width_center * (start_col + start_col + 1)
        end_x_pos = cell_width_center * (start_col + start_col + 3)
        start_y_pos = (cell_height_center * (start_row + start_row + 1)) + self.top_offset
        end_y_pos = start_y_pos

        for i in range(total_occurrences - 1):
            pg.draw.line(
                surface=self.display,
                color=self.win_line_color,
                start_pos=(start_x_pos + ((cell_width_center * 2) * i), start_y_pos),
                end_pos=(end_x_pos + ((cell_width_center * 2) * i), end_y_pos),
                width=self.win_line_thickness,
            )


    def draw_vertical_win_line(self, start_row: int, start_col: int, board_size: int, total_occurrences: int) -> None:
        cell_width_center, cell_height_center = self.get_cell_midpoint(board_size)

        start_x_pos = cell_width_center * (start_col + start_col + 1)
        end_x_pos = start_x_pos
        start_y_pos = cell_height_center * (start_row + start_row + 1) + self.top_offset
        end_y_pos = cell_height_center * (start_row + start_row + 3) + self.top_offset

        for i in range(total_occurrences - 1):
            pg.draw.line(
                surface=self.display,
                color=self.win_line_color,
                start_pos=(start_x_pos, start_y_pos + ((cell_height_center * 2) * i)),
                end_pos=(end_x_pos, end_y_pos + ((cell_height_center * 2) * i)),
                width=self.win_line_thickness,
            )


    def draw_anti_diagonal_win_line(self, start_row: int, start_col: int, board_size: int, total_occurrences: int) -> None:
        cell_width_center, cell_height_center = self.get_cell_midpoint(board_size)

        start_x_pos = cell_width_center * (start_col + start_col + 1)
        end_x_pos = cell_width_center * (start_col + start_col + 3)
        start_y_pos = (cell_height_center * (start_row + start_row + 1)) + self.top_offset
        end_y_pos = (cell_height_center * ((start_row + start_row - 1))) + self.top_offset

        for i in range(total_occurrences - 1):
            pg.draw.line(
                surface=self.display,
                color=self.win_line_color,
                start_pos=(start_x_pos + ((cell_width_center * 2) * i), start_y_pos - (cell_height_center * 2) * i),
                end_pos=(end_x_pos + ((cell_width_center * 2) * i), end_y_pos - (cell_height_center * 2) * i),
                width=self.win_line_thickness,
            )


    def draw_main_diagonal_win_line(self, start_row: int, start_col: int, board_size: int, total_occurrences: int) -> None:
        cell_width_center, cell_height_center = self.get_cell_midpoint(board_size)

        start_x_pos = cell_width_center * (start_col + start_col + 1)
        end_x_pos = cell_width_center * (start_col + start_col + 3)
        start_y_pos = (cell_height_center * (start_row + start_row + 1)) + self.top_offset
        end_y_pos = (cell_height_center * (start_row + start_row + 3)) + self.top_offset

        for i in range(total_occurrences - 1):
            pg.draw.line(
                surface=self.display,
                color=self.win_line_color,
                start_pos=(start_x_pos + ((cell_width_center * 2) * i), start_y_pos + ((cell_height_center * i) * 2)),
                end_pos=(end_x_pos + ((cell_width_center * 2) * i), end_y_pos + ((cell_height_center * i) * 2)),
                width=self.win_line_thickness,
            )
