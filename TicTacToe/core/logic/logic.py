from typing import List, Tuple

from core.configs import GameConfigs


class GameLogic():

    def __init__(self, app) -> None:
        from main import Application

        self.app: Application = app

        # Attributes
        self.game_board:                 List[List[str]] = None
        self.board_size:                 int             = None
        self.current_symbol:             str             = None
        self.consecutive_symbols_to_win: int             = None
        
        self.update()


    def update(self) -> None:
        _configs: GameConfigs = self.app.configs

        # Update all attributes
        self.board_size = _configs.BOARD_SIZE
        self.current_symbol = _configs.START_SYMBOL
        self.consecutive_symbols_to_win = _configs.CONSECUTIVE_SYMBOLS_TO_WIN

        self.game_board = self.empty_tictactoe_board()
        

    def empty_tictactoe_board(self) -> List[List[str]]:
        return [['' for _ in range(self.board_size)] for _ in range(self.board_size)]


    def new_game(self) -> None:
        if self.consecutive_symbols_to_win > self.board_size:
            print(f"\nWARNING - - - > Invalid ['consecutive_symbols_to_win'] value set in ['configs']!")
            print(f"\nWARNING - - - > ['consecutive_symbols_to_win'] was set to {self.board_size}!")

            # Override 'consecutive_symbols_to_win' to 'board_size'
            self.consecutive_symbols_to_win = self.board_size

        self.game_board = self.empty_tictactoe_board()

        # Reloading the screen
        self.app.screen.update_display()
        self.app.screen.blit_display()
        self.app.screen.draw_tictactoe_board(self.board_size)


    def next_move(self, already_won: bool) -> None:
        row, col = self.app.screen.get_mouse_pos(self.board_size)

        if row == -1 and col == -1:
            print("\nWARNING - - - > Out of the game screen!")

        elif self.game_board[row][col] == '' and not already_won:
            self.app.screen.draw_symbol(row, col, self.board_size, self.current_symbol)
            self.game_board[row][col] = self.current_symbol
            self.current_symbol = "O" if self.current_symbol == "X" else "X"


    def check_win_or_draw(self) -> Tuple[bool, str]: 
        symbol_to_check = "O" if self.current_symbol == "X" else "X"

        # Check for a horizontal win
        for row in range(self.board_size):
            consecutive_symbols_count = 0
            start_row = row
            for col in range(self.board_size):
                start_col = col - consecutive_symbols_count

                if self.game_board[row][col] == symbol_to_check:
                    consecutive_symbols_count += 1

                    if consecutive_symbols_count == self.consecutive_symbols_to_win:
                        game_board_line = self.get_game_board_line(start_row, start_col, "horizontal")
                        total_occurrences = self.get_total_occurrences(game_board_line, symbol_to_check)

                        self.app.screen.draw_horizontal_win_line(start_row, start_col, self.board_size, total_occurrences)
                        return True, f"Horizontal victory by: {symbol_to_check}!"
                else:
                    consecutive_symbols_count = 0

        # Check for a vertical win
        for col in range(self.board_size):
            consecutiveSymbolsCount = 0
            start_col = col
            for row in range(self.board_size):
                start_row = row - consecutiveSymbolsCount

                if self.game_board[row][col] == symbol_to_check:
                    consecutiveSymbolsCount += 1

                    if consecutiveSymbolsCount == self.consecutive_symbols_to_win:
                        game_board_line = self.get_game_board_line(start_row, start_col, "vertical")
                        total_occurrences = self.get_total_occurrences(game_board_line, symbol_to_check)

                        self.app.screen.draw_vertical_win_line(start_row, start_col, self.board_size, total_occurrences)
                        return True, f"Vertical victory by: {symbol_to_check}!"
                else:
                    consecutiveSymbolsCount = 0

        # Check for a anti-diagonal win
        consecutiveSymbolsCount = 0
        for row in range(self.board_size - 1, -1, -1):
            for col in range(self.board_size - 1, -1, -1):

                if self.game_board[row][col] == symbol_to_check:
                    consecutiveSymbolsCount = 0

                    for i in range(self.consecutive_symbols_to_win):
                        if row + i < self.board_size and col - i >= 0:
                            if self.game_board[row + i][col - i] == symbol_to_check:
                                consecutiveSymbolsCount += 1
                                start_row = row + i
                                start_col = col - i

                    if consecutiveSymbolsCount == self.consecutive_symbols_to_win:
                        game_board_line = self.get_game_board_line(start_row, start_col, "anti-diagonal")
                        total_occurrences = self.get_total_occurrences(game_board_line, symbol_to_check)

                        self.app.screen.draw_anti_diagonal_win_line(start_row, start_col, self.board_size, total_occurrences)
                        return True, f"Anti-diagonal victory by: {symbol_to_check}!"

                    consecutiveSymbolsCount = 0

        # Check for a main-diagonal win
        consecutiveSymbolsCount = 0
        for row in range(self.board_size):
            for col in range(self.board_size):

                if self.game_board[row][col] == symbol_to_check:
                    consecutiveSymbolsCount = 0

                    for i in range(self.consecutive_symbols_to_win):
                        if row + i < self.board_size and col + i < self.board_size:
                            if self.game_board[row + i][col + i] == symbol_to_check:
                                consecutiveSymbolsCount += 1
                                start_row = row
                                start_col = col

                    if consecutiveSymbolsCount == self.consecutive_symbols_to_win:
                        game_board_line = self.get_game_board_line(row, col, "main-diagonal")
                        total_occurrences = self.get_total_occurrences(game_board_line, symbol_to_check)

                        self.app.screen.draw_main_diagonal_win_line(start_row, start_col, self.board_size, total_occurrences)
                        return True, f"Main-diagonal victory by: {symbol_to_check}!"

                    consecutiveSymbolsCount = 0

        # Check for a draw
        if all(self.game_board[row][col] != "" for row in range(self.board_size) for col in range(self.board_size)):
            return True, "It's a draw!"

        return False, None


    def get_game_board_line(self, start_row: int, start_col: int, direction: str) -> List[str]:
        game_board_line: List[str] = []

        if direction == "horizontal":
            for i in range(self.board_size):
                game_board_line.append(self.game_board[start_row][i])

        elif direction == "vertical":
            for i in range(self.board_size):
                game_board_line.append(self.game_board[i][start_col])

        elif direction == "main-diagonal":
            for i in range(self.board_size):
                if (start_row + i >= self.board_size) or (start_col + i >= self.board_size):
                    break  
                else:
                    game_board_line.append(self.game_board[start_row + i][start_col + i])

        elif direction == "anti-diagonal":
            for i in range(self.board_size):
                if ((start_row - i) < 0) or ((start_col + i) >= self.board_size):
                    break
                else:
                    game_board_line.append(self.game_board[start_row - i][start_col + i])

        return game_board_line


    def get_total_occurrences(self, game_board_line: List[str], symbol: str) -> int:
        total_occurrences: int = 0
        first_occurrence: int = 0
        count: int = 0

        for i in range(len(game_board_line)):
            if game_board_line[i] == symbol:
                count += 1
                if count == 1:
                    first_occurrence = i
                elif count == self.consecutive_symbols_to_win:
                    break
            else:
                count = 0

        # Verify the total occurrence of a given symbol in 'game_board_line'
        for i in range(len(game_board_line)):
            if game_board_line[i] == symbol:
                total_occurrences += 1
                if total_occurrences == self.consecutive_symbols_to_win:
                    break

        # Reverify the total occurrence of a given symbol in case there's more ahead
        for i in range(first_occurrence + total_occurrences - 1, len(game_board_line) - 1):
            if game_board_line[i + 1] == symbol:
                total_occurrences += 1
            else:
                break

        return total_occurrences
