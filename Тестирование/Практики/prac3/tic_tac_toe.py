from enum import Enum
from collections.abc import Callable
import re


class PlaceTakenError(Exception):
    pass


class GameState(Enum):
    MENU = 1
    INPUT_MODE = 2
    FIRST_PLAYER = 3
    SECOND_PLAYER = 4
    EXIT = 5


class GameMode(Enum):
    CLASSIC = 1
    EXTENDED = 2


class Transition:

    def __init__(self, current_state: GameState,
                 _input: str | Callable[[str], bool], next_state: GameState):
        self.current_state = current_state
        self.input = _input
        self.next_state = next_state

    def __call__(self, _input: str) -> GameState | None:
        if type(self.input) is str and self.input == _input:
            return self.next_state

        elif callable(self.input) and self.input(_input):
            return self.next_state

        return None


class TicTacToe:

    def __init__(self):
        self.previous_state: GameState | None = None
        self.state = GameState.MENU
        self.mode = GameMode.CLASSIC
        self.table = [[0 for _ in range(3)] for _ in range(3)]
        self.transitions = [
            Transition(GameState.MENU, '1', GameState.INPUT_MODE),
            Transition(GameState.MENU, '2', GameState.FIRST_PLAYER),
            Transition(GameState.INPUT_MODE, lambda x: re.match(r'[1-2]', x),
                       GameState.MENU),
            Transition(GameState.FIRST_PLAYER,
                       lambda x: re.match(r'[1-5] [1-5]', x),
                       GameState.SECOND_PLAYER),
            Transition(GameState.SECOND_PLAYER,
                       lambda x: re.match(r'[1-5] [1-5]', x),
                       GameState.FIRST_PLAYER),
            Transition(GameState.MENU, '3', GameState.EXIT)
        ]

    def change_state(self, input_command: str):
        next_state = None
        for transition in self.transitions:
            if transition.current_state == self.state:
                next_state = transition(input_command)

            if next_state is not None:
                self.previous_state = self.state
                self.state = next_state
                break
        if next_state is None:
            raise ValueError('Введена неправильная команда')

    def print_board(self):
        if self.mode == GameMode.CLASSIC:
            n = 3
        elif self.mode == GameMode.EXTENDED:
            n = 5

        board_lines = []
        for i in range(n):
            board_line = []
            for j in range(n):
                elem = self.table[i][j]
                elem = "x" if elem == 1 else "o" if elem == -1 else " "
                cell = f" {elem} "
                board_line.append(cell)
            board_line = "||".join(board_line)
            board_line += "\n"
            board_lines.append(board_line)

        border = "=" * (3 * n + 2 * (n - 1)) + "\n"

        board = border.join(board_lines)
        return board

    def change_mode(self, input_command: str):
        if input_command == '1':
            self.mode = GameMode.CLASSIC
            n = 3
        elif input_command == '2':
            self.mode = GameMode.EXTENDED
            n = 5

        self.table = [[0 for _ in range(n)] for _ in range(n)]

    def handle_game_input(self, position: str):
        if self.mode == GameMode.CLASSIC:
            n = 3
        elif self.mode == GameMode.EXTENDED:
            n = 5

        if self.previous_state == GameState.FIRST_PLAYER:
            elem = 1
        elif self.previous_state == GameState.SECOND_PLAYER:
            elem = -1

        i, j = map(lambda x: int(x) - 1, position.split())
        if i in range(n) and j in range(n) and self.table[i][j] == 0:
            self.table[i][j] = elem
        else:
            self.state = self.previous_state
            if i not in range(n) or j not in range(n):
                raise ValueError('Введены некорректные координаты')
            elif self.table[i][j] != 0:
                raise PlaceTakenError('Место уже занято')

    def post_change_state(self, input_command: str):
        match self.previous_state:
            case GameState.INPUT_MODE:
                self.change_mode(input_command)
            case GameState.FIRST_PLAYER:
                self.handle_game_input(input_command)
            case GameState.SECOND_PLAYER:
                self.handle_game_input(input_command)
            case GameState.MENU:
                pass

    def check_game_end(self):
        if self.mode == GameMode.CLASSIC:
            n = 3
        elif self.mode == GameMode.EXTENDED:
            n = 5
        if self.previous_state == GameState.FIRST_PLAYER:
            elem = 1
        elif self.previous_state == GameState.SECOND_PLAYER:
            elem = -1

        row_win, col_win, diag1_win, diag2_win = 0, 0, 0, 0
        if any([all(cell == 1 for cell in row) for row in self.table]) or \
           any([all(cell == -1 for cell in row) for row in self.table]):
            row_win = elem

        if any(all(cell == 1 for cell in col) for col in zip(*self.table)) or \
           any(all(cell == -1 for cell in col) for col in zip(*self.table)):
            col_win = elem

        if all(self.table[i][i] == 1 for i in range(n)) or \
            all(self.table[i][i] == -1 for i in range(n)):
            diag1_win = elem
        if all(self.table[i][n - i - 1] == 1 for i in range(n)) or \
            all(self.table[i][n - i - 1] == -1 for i in range(n)):
            diag2_win = elem

        if any(elem == 1 for elem in [row_win, col_win, diag1_win, diag2_win]):
            result = 1
        elif any(elem == -1
                 for elem in [row_win, col_win, diag1_win, diag2_win]):
            result = -1
        elif all(self.table[i][j] != 0 for i in range(n) for j in range(n)):
            result = 2
        else:
            result = 0
        
        if result != 0:
            self.state = GameState.MENU
            self.clear_table()
        return result

    def create_prompt(self):
        match self.state:
            case GameState.MENU:
                return '1) Изменить режим игры\n2) Запустить игру\n3) Выйти из игры\n'
            case GameState.INPUT_MODE:
                return ('Введите режим игры:\n'
                        '1) Классический (3 x 3)\n'
                        '2) Расширенный (5 x 5)\n')
            case GameState.FIRST_PLAYER:
                return 'Первый игрок, введите позицию: '
            case GameState.SECOND_PLAYER:
                return 'Второй игрок, введите позицию: '

    def clear_table(self):
        if self.mode == GameMode.CLASSIC:
            n = 3
        elif self.mode == GameMode.EXTENDED:
            n = 5

        self.table = [[0 for _ in range(n)] for _ in range(n)]

    def game_cycle(self):
        error = False
        while True:
            if self.state in [GameState.FIRST_PLAYER,
                              GameState.SECOND_PLAYER] and \
                                  not error:
                print(self.print_board())

            input_command = input(self.create_prompt())
            try:
                self.change_state(input_command)
                error = False
            except ValueError as e:
                print(e)
                error = True
                continue

            if self.state == GameState.EXIT:
                break

            try:
                self.post_change_state(input_command)
                error = False
            except (ValueError, PlaceTakenError) as e:
                print(e)
                error = True
                continue

            if self.state in [GameState.FIRST_PLAYER, GameState.SECOND_PLAYER]:
                result = self.check_game_end()
                if result != 0:
                    print(self.print_board())
                if result == 1:
                    print('Победил первый игрок!')
                elif result == -1:
                    print('Победил второй игрок!')
                elif result == 2:
                    print('Победила дружба)')


def main():
    game = TicTacToe()
    game.game_cycle()


if __name__ == '__main__':
    main()
