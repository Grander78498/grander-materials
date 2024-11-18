import unittest
from tic_tac_toe import TicTacToe, GameState, PlaceTakenError


class TestChangeState(unittest.TestCase):
    def setUp(self) -> None:
        self.game = TicTacToe()

    def test_menu_state(self) -> None:
        self.assertEqual(self.game.state, GameState.MENU)

    def test_change_to_input(self) -> None:
        self.game.change_state('1')
        self.assertEqual(self.game.state, GameState.INPUT_MODE)

    def test_input_game_mode(self) -> None:
        possible_inputs = [('1', GameState.MENU), ('2', GameState.MENU),
                           ('0', ValueError), ('asjdgs', ValueError)]
        for _input, result in possible_inputs:
            self.game.state = GameState.INPUT_MODE
            if result is ValueError:
                with self.assertRaises(ValueError):
                    self.game.change_state(_input)

            else:
                self.game.change_state(_input)
                self.assertEqual(self.game.state, result)

    def test_start_game(self) -> None:
        self.game.change_state('2')
        self.assertEqual(self.game.state, GameState.FIRST_PLAYER)

    def test_change_player(self):
        self.game.change_state('2')
        self.game.change_state('1 1')
        self.assertEqual(self.game.state, GameState.SECOND_PLAYER)
        self.game.change_state('4 3')
        self.assertEqual(self.game.state, GameState.FIRST_PLAYER)
        with self.assertRaises(ValueError):
            self.game.change_state('6 6')


class TestPrintBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.game = TicTacToe()

    def test_print_classic(self):
        self.assertEqual(self.game.print_board(), "   ||   ||   \n"
                                                  "=============\n"
                                                  "   ||   ||   \n"
                                                  "=============\n"
                                                  "   ||   ||   \n")
        
    def test_print_extended(self):
        self.game.change_mode('2')
        self.assertEqual(self.game.print_board(), "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n")
        
    def test_print_classic_with_symbols(self):
        self.game.table[0][1] = 1
        self.assertEqual(self.game.print_board(), "   || x ||   \n"
                                                  "=============\n"
                                                  "   ||   ||   \n"
                                                  "=============\n"
                                                  "   ||   ||   \n")
        self.game.table[1][2] = -1
        self.assertEqual(self.game.print_board(), "   || x ||   \n"
                                                  "=============\n"
                                                  "   ||   || o \n"
                                                  "=============\n"
                                                  "   ||   ||   \n")
        self.game.table[2][1] = 1
        self.assertEqual(self.game.print_board(), "   || x ||   \n"
                                                  "=============\n"
                                                  "   ||   || o \n"
                                                  "=============\n"
                                                  "   || x ||   \n")

    def test_print_extended_with_symbols(self):
        self.game.change_mode('2')
        self.game.table[0][0] = -1
        self.assertEqual(self.game.print_board(), " o ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n")
        self.game.table[0][4] = 1
        self.assertEqual(self.game.print_board(), " o ||   ||   ||   || x \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n")
        self.game.table[2][3] = 1
        self.assertEqual(self.game.print_board(), " o ||   ||   ||   || x \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   || x ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n")
        self.game.table[4][1] = -1
        self.assertEqual(self.game.print_board(), " o ||   ||   ||   || x \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   || x ||   \n"
                                                  "=======================\n"
                                                  "   ||   ||   ||   ||   \n"
                                                  "=======================\n"
                                                  "   || o ||   ||   ||   \n")


class TestInputPosition(unittest.TestCase):
    def setUp(self) -> None:
        self.game = TicTacToe()

    def test_input_position_classic(self):
        positions = [('1 1', 0, 0), ('2 3', 1, 2), ('3 1', 2, 0),
                     ('1 4', ValueError), ('1 1', PlaceTakenError), ('2 2', 1, 1)]
        table = [[0 for _ in range(3)] for _ in range(3)]
        self.game.change_state('2')
        k = 0
        for index, (position, *result) in enumerate(positions):
            self.game.change_state(position)
            if result[0] is ValueError or result[0] is PlaceTakenError:
                k += 1
                with self.assertRaises(result[0]):
                    self.game.handle_game_input(position)
            else:
                i, j = result
                table[i][j] = (-1) ** (index - k)
                self.game.handle_game_input(position)
                self.assertEqual(self.game.table, table)

    def test_input_position_extended(self):
        positions = [('1 1', 0, 0), ('2 3', 1, 2), ('3 1', 2, 0),
                     ('1 4', 0, 3), ('1 1', PlaceTakenError), ('2 2', 1, 1)]
        table = [[0 for _ in range(5)] for _ in range(5)]
        self.game.change_state('2')
        self.game.change_mode('2')

        k = 0
        for index, (position, *result) in enumerate(positions):
            self.game.change_state(position)
            if result[0] is ValueError or result[0] is PlaceTakenError:
                k += 1
                with self.assertRaises(result[0]):
                    self.game.handle_game_input(position)
            else:
                i, j = result
                table[i][j] = (-1) ** (index - k)
                self.game.handle_game_input(position)
                self.assertEqual(self.game.table, table)


class TestCheckGameEnd(unittest.TestCase):
    def setUp(self) -> None:
        self.game = TicTacToe()
        self.game.change_state('2')
        self.game.post_change_state('2')

    def mock_playing(self, commands, result):
        for command in commands:
            self.game.change_state(command)
            self.game.post_change_state(command)
        self.assertEqual(self.game.check_game_end(), result)

    # ================

    def test_check_without_win_1(self):
        commands = ['2 2', '3 1', '2 3']
        self.mock_playing(commands, 0)

    def test_check_without_win_2(self):
        commands = ['1 1', '2 3', '2 2', '3 3']
        self.mock_playing(commands, 0)

    def test_check_without_win_3(self):
        commands = ['1 2', '3 1', '2 2']
        self.mock_playing(commands, 0)

    # ================

    def test_check_first_win_1(self):
        commands = ['1 1', '2 1', '1 2', '2 2', '1 3']
        self.mock_playing(commands, 1)

    def test_check_first_win_2(self):
        commands = ['1 1', '1 2', '2 1', '2 2', '3 1']
        self.mock_playing(commands, 1)

    def test_check_first_win_3(self):
        commands = ['1 1', '2 1', '2 2', '1 2', '3 3']
        self.mock_playing(commands, 1)

    def test_check_first_win_4(self):
        commands = ['1 3', '2 1', '2 2', '1 2', '3 1']
        self.mock_playing(commands, 1)

    # ================

    def test_check_second_win_1(self):
        commands = ['1 1', '2 1', '1 2', '2 2', '3 1', '2 3']
        self.mock_playing(commands, -1)

    def test_check_second_win_2(self):
        commands = ['1 1', '1 2', '2 1', '2 2', '1 3', '3 2']
        self.mock_playing(commands, -1)

    def test_check_second_win_3(self):
        commands = ['1 2', '1 1', '2 1', '2 2', '3 1', '3 3']
        self.mock_playing(commands, -1)

    def test_check_second_win_4(self):
        commands = ['1 2', '1 3', '2 1', '2 2', '3 3', '3 1']
        self.mock_playing(commands, -1)

    # ================

    def test_check_draw(self):
        commands = ['1 1', '1 2', '2 2', '3 3', '1 3', '2 1', '3 2', '3 1', '2 3']
        self.mock_playing(commands, 2)
