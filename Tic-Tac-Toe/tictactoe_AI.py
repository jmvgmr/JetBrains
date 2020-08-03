import math
import random

LEVELS = ['user', 'easy', 'medium', 'hard']


class TicTacToe:
    def __init__(self):
        self.board = self.make_board()
        self.current_winner = None

    @staticmethod
    def make_board():
        return ['_'] * 9

    def print_board(self):
        print('---------')
        for row in [self.board[i * 3: (i + 1) * 3] for i in range(3)]:
            print('|', ' '.join(row).replace('_', ' '), '|')
        print('---------')

    def make_move(self, square, player):
        if self.board[square] == '_':
            self.board[square] = player
            if self.winner(square, player):
                self.current_winner = player
            return True
        return False

    def winner(self, square, player):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([symbol == player for symbol in row]):
            return True
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([symbol == player for symbol in column]):
            return True
        # Check diagonals
        if square % 2 == 0:
            diag_1 = [self.board[i] for i in [0, 4, 8]]
            if all([symbol == player for symbol in diag_1]):
                return True
            diag_2 = [self.board[i] for i in [2, 4, 6]]
            if all([symbol == player for symbol in diag_2]):
                return True
        return False

    def empty_squares(self):
        return '_' in self.board

    def num_empty_squares(self):
        return self.board.count('_')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == '_']


class Player:
    def __init__(self, player):
        self.player = player

    def get_move(self, game):
        pass


class Human(Player):
    def __init__(self, player):
        super().__init__(player)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            coord = input('Enter the coordinates: ').split()
            try:
                x, y = int(coord[0]), int(coord[1])
                if not (x in (1, 2, 3) and y in (1, 2, 3)):
                    print('Coordinates should be from 1 to 3')
                    continue
                val = x - 3 * y + 8
                if val not in game.available_moves():
                    print('This cell is occupied! Choose another one!')
                    continue
                valid_square = True
            except (ValueError, IndexError):
                print('You should enter numbers!')
        return val


class EasyAI(Player):
    def __init__(self, player):
        super().__init__(player)
        self.player = player

    def get_move(self, game):
        print('Making move level "easy"')
        square = random.choice(game.available_moves())
        return square


class MediumAI(Player):
    def __init__(self, player):
        super().__init__(player)
        self.player = player

    def get_move(self, game):
        print('Making move level "medium"')
        rival = 'X' if self.player == 'O' else 'O'
        # if len(game.available_moves()) == 9:
        square = random.choice(game.available_moves())
        return square


class HardAI(Player):
    def __init__(self, player):
        super().__init__(player)

    def get_move(self, game):
        print('Making move level "hard"')
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.player)['position']
        return square

    def minimax(self, state, player):
        """

        :type state: TicTacToe
        """
        max_player = self.player
        other_player = 'X' if player == 'O' else 'O'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}   # Maximize
        else:
            best = {'position': None, 'score': math.inf}    # Minimize

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)   # Simulate one more move

            # Undo move
            state.board[possible_move] = '_'
            state.current_winner = None
            sim_score['position'] = possible_move   # Optimal next move

            if player == max_player: # X max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


def play(game, x_player, o_player, print_game=True):
    """
    :type o_player: Player
    :type x_player: Player
    :type game: TicTacToe
    """
    if print_game:
        game.print_board()

    player = 'X'
    while game.empty_squares():
        if player == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, player):
            if print_game:
                # print(f'{player} makes a move to square {square}')
                game.print_board()
                # print('')
            if game.current_winner:
                if print_game:
                    print(player + ' wins')
                return player
            player = 'X' if player == 'O' else 'O'
    if print_game:
        print('Draw')


def get_command():
    while True:
        command = input('Input command: ').split()
        if command[0] == 'exit':
            return
        elif len(command) == 3 and command[0] == 'start' and command[1] in LEVELS and command[2] in LEVELS:
            break
        else:
            print('Bad parameters!')

    x_player = HardAI('X') if command[1] == 'hard' else EasyAI('X') if command[1] == 'easy' else MediumAI('X') if command[1] == 'medium' else Human('X')
    o_player = HardAI('O') if command[1] == 'hard' else EasyAI('O') if command[1] == 'easy' else MediumAI('O') if command[1] == 'medium' else Human('O')

    t = TicTacToe()
    play(t, x_player, o_player)

get_command()
