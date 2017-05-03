from sys import stdin, stdout, stderr
import numpy as np
import time as time
import board_helper as bh


class Bot(object):
    def __init__(self):
        # Stores game settings
        self.settings = dict()

        # Current round
        self.round = 1

        # The game board
        self.field = np.zeros((6, 7), dtype=np.uint8)

        # What time you have to make your move by
        self.timeout_time = None

        # Heuristic values
        self.heuristic_values = {'1-row': 0, '2-row': 3, '3-row': 20, '4-row': 100}

        # Whether to show debug output in stderr
        self.DEBUG_OUTPUT = False

    def print_debug(self, value):
        if self.DEBUG_OUTPUT:
            stderr.write("* " + str(value) + '\n')

    def rows(self):
        return self.settings['field_rows']

    def columns(self):
        return self.settings['field_columns']

    def bot_id(self):
        return self.settings['your_botid']

    def opponent_id(self):
        return 2 if self.bot_id() == 1 else 1

    def current_time_milli(self):
        return int(time.time() * 1000)

    def time_left(self):
        """Returns time left until timeout is reached."""
        return self.timeout_time - self.current_time_milli()

    def update_timeout_time(self, millis):
        """Updates the timeout time using the parameters received from the engine."""
        self.timeout_time = self.current_time_milli() + millis

    def set_settings(self, args, value):
        """Defines the settings vars."""
        if args in ('timebank', 'time_per_move', 'your_botid', 'field_columns', 'field_rows'):
            value = int(value)
        self.settings[args] = value

        self.print_debug(str(args + ' = ' + str(value)))

    def update_board(self, args, value):
        """Updates the board with info from engine."""
        if args == 'round':
            self.round = int(value)
        elif args == 'field':
            self.field = np.fromstring(value.replace(';', ','), dtype=int, sep=',').reshape(self.rows(), self.columns())
            self.print_debug(self.field)

    def can_move(self, column):
        return self.field[0][column] == 0

    def make_turn(self, time_left):
        """Decides where to place the token."""
        self.print_debug('time left:' + str(time_left))
        self.update_timeout_time(time_left)

        # Places disk in middle as first move if available
        if self.round in [1, 2] and (self.bot_id() == 1 or self.field[5][3] == 0):
            return self.place_token(3)

        depth = 3
        minimax = self.minimax(depth=depth, node=np.copy(self.field), max_player=True)
        print 'Column ' + str(minimax[1]) + ' has a heuristic of ' + str(minimax[0])

        return self.place_token(minimax[1])

    def minimax(self, depth, node, max_player):
        # TODO Store the explored nodes to save CPU time?

        # If the node is a leaf or terminal node, return the value (start going back up the recursive function)
        if depth == 0 or bh.is_game_won(node):
            return [self.eval_board(board=node)]

        best_move = 3

        # ---MAX FUNCTION---
        if max_player:
            # Sets best_value to lowest possible value (opponent win)
            best_value = -self.heuristic_values['4-row']

            # Loads the possible moves
            moves = self.possible_moves(board=node, player_id=self.bot_id())
            for i in range(len(moves)):
                # Goes down one node further to evaluate the value of the parent node (the current node)
                value = self.minimax(depth=depth - 1, node=moves[i], max_player=False)[0]

                # Sets the parent node to the highest value
                if value > best_value:
                    best_value = value
                    best_move = i
            return best_value, best_move

        # ---MIN FUNCTION---
        else:
            # Sets best_value to highest possible value (my win)
            best_value = self.heuristic_values['4-row']

            moves = self.possible_moves(board=node, player_id=self.opponent_id())
            for i in range(len(moves)):
                value = self.minimax(depth=depth - 1, node=moves[i], max_player=True)[0]
                if value < best_value:
                    best_value = value
                    best_move = i
            return best_value, best_move

    def possible_moves(self, board, player_id):
        """Returns array or possible moves given a board state"""
        moves = []
        for c in range(self.columns()):
            if self.can_move(column=c):
                moves.append(self.simulate_move(column=c, board=board, player_id=player_id))
        return moves

    def simulate_move(self, column, board, player_id):
        """Returns board with token placed in specific column"""
        board = np.copy(board)
        if self.can_move(column):
            # Since the bottom row is index 5, starts at 5 and decrements through 0
            for r in range(self.rows() - 1, -1, -1):
                if board[r][column] == 0:
                    board[r][column] = player_id
                    return board

    def eval_board(self, board):
        """Returns the heuristic value of a board state"""
        # TODO: Use genetic algorithm to determine weights? https://goo.gl/T57ELB
        # TODO: In situations such as 1,1,1,0, the bot won't place a token in 0 and take the win.
        totals = {self.bot_id(): 0, self.opponent_id(): 0}

        # Checking sequences
        for player_id in totals.keys():
            transposed_board = [list(x) for x in zip(*board)]
            # Top left to bottom right diagonals going like \
            pos_diagonals = [np.diagonal(board, x) for x in range(-2, 4)]
            # Bottom left to top right diagonals going like /
            neg_diagonals = [np.diagonal(board[::-1], x) for x in range(-2, 4)]

            board_orientations = (
                board,
                transposed_board,
                pos_diagonals,
                neg_diagonals
            )

            for orientation in board_orientations:
                for row in orientation:
                    for sequence_len in bh.sequences(row, player_id):
                        totals[player_id] += self.heuristic_values[str(sequence_len) + '-row']

        return totals[self.bot_id()] - totals[self.opponent_id()]

    def place_token(self, column):
        """Writes the move into stdout stream."""
        stdout.write("place_disc %d\n" % column)
        stdout.flush()
        return column

    def feed(self, val):
        engine_in = val.split()

        if engine_in[0] == "settings":
            self.set_settings(args=engine_in[1], value=engine_in[2])
        elif engine_in[0] == "update":
            self.update_board(args=engine_in[2], value=engine_in[3])
        elif engine_in[0] == "action":
            return self.make_turn(time_left=int(engine_in[2]))

    def run(self):
        """ Reads and translates the engine input into actions. """
        while not stdin.closed:
            raw_line = stdin.readline()

            # End of file check
            if len(raw_line) == 0:
                break

            line = raw_line.strip()

            # Empty lines can be ignored
            if len(line) == 0:
                continue

            self.feed(line)


if __name__ == '__main__':
    Bot().run()
