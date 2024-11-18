from behave import given, then, when
from tic_tac_toe import TicTacToe, GameState, PlaceTakenError


@given('игра запущена')
def step_game_launched(context):
    context.game = TicTacToe()
    context.game.change_state('2')


@given('режим игры {mode}')
def step_game_mode(context, mode):
    if mode == 'стандартный':
        context.game.change_mode('1')
    elif mode == 'расширенный':
        context.game.change_mode('2')


@when('{player} игрок заполнил ячейку {i} {j}')
def step_cell_filled(context, player, i, j):
    position = f'{i} {j}'
    context.is_failed = False
    try:
        context.game.change_state(position)
    except ValueError:
        context.is_failed = True
    try:
        context.game.post_change_state(position)
    except (ValueError, PlaceTakenError):
        context.is_failed = True


@when('игроки сделали следующие ходы')
def step_many_turns(context):
    for row in context.table:
        position = f"{row['i']} {row['j']}"
        context.game.change_state(position)
        context.game.post_change_state(position)


@then('игра {status}')
def step_game_status(context, status):
    if status == 'продолжается':
        assert context.game.state in [GameState.FIRST_PLAYER, GameState.SECOND_PLAYER]
    elif status == 'завершилась ничьёй':
        assert context.game.check_game_end() == 2


@then('ходит {player} игрок')
def step_current_player(context, player):
    if player == 'первый':
        assert context.game.state == GameState.FIRST_PLAYER
    elif player == 'второй':
        assert context.game.state == GameState.SECOND_PLAYER

@then('выиграл {player} игрок')
def step_winner(context, player):
    if player == 'первый':
        assert context.game.check_game_end() == 1
    elif player == 'второй':
        assert context.game.check_game_end() == -1
