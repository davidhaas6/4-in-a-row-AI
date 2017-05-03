from itertools import groupby, chain
import numpy as np
import bot
from random import randint
import time

NONE = '0'
player_1 = '1'
player_2 = '2'
intro = ["settings timebank 10000",
         "settings time_per_move 500",
         "settings player_names player1,player2",
         "settings your_bot player1",
         "settings field_columns 7",
         "settings field_rows 6"]


def write(val):
    return AI.feed(val)


def write_updates(field, round_n):
    write('update game round ' + str(round_n))
    write('update game field ' + field)


def format_board(board):
    flat_arr = np.swapaxes(np.asarray(board), 0, 1).flatten()
    field = ''
    count = 1
    for i in flat_arr:
        field += str(i)
        if count % 7 == 0:
            field += ';'
        else:
            field += ','
        count += 1
    return field[:-1]


def diagonals_pos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]


def diagonals_neg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]


class Game:
    def __init__(self, cols=7, rows=6, required_to_win=4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = required_to_win
        self.board = [[NONE] * rows for _ in range(cols)]

    def get_board(self):
        return self.board

    def insert(self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            raise Exception('Column is full')
        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
        # self.check_for_win()

    def check_for_win(self):
        """Check the current board for a winner."""
        w = self.get_winner()
        if w:
            print '\n' + ('#' * 19 + '\n') * 3
            self.print_board()
            print '\n***************\nPlayer ' + str(w) + ' wins!\n***************\n'
            return True

    def get_winner(self):
        """Get the winner on the current board."""
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonals_pos(self.board, self.cols, self.rows),  # positive diagonals
            diagonals_neg(self.board, self.cols, self.rows)  # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    def print_board(self):
        """Print the board."""
        print('--'.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join(str(self.board[x][y]) for x in range(self.cols)))


if __name__ == '__main__':
    g = Game()
    turn = player_1
    AI = bot.Bot()
    round_num = 1
    for i in intro:
        write(i)

    your_id = str(randint(1, 2))
    bot_id = '2' if your_id == '1' else '1'
    write("settings your_botid " + str(bot_id))

    print '*** YOU ARE PLAYER ' + your_id + ' ***'

    while g.check_for_win() is None:
        write_updates(format_board(g.get_board()), round_num)
        row = -1
        time.sleep(.2)
        print ''
        g.print_board()

        if turn == bot_id:
            row = write('action move 10000')
        else:
            row = input('Your turn:')

        g.insert(int(row), turn)
        turn = player_2 if turn == player_1 else player_1
        round_num += 1
