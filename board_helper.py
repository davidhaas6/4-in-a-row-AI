import numpy as np
from itertools import chain, groupby


def contains(parent_list, sub_list):
    """See if a list contains the exact sequence of a sublist"""
    for i in range(len(parent_list) - len(sub_list) + 1):
        print parent_list[i:i + len(sub_list)]
        if parent_list[i:i + len(sub_list)] == sub_list:
            return True
    return False


def sequences(arr, val):
    """Returns array of sequence lengths of a value in an array"""
    # List of lengths of sequences
    seq = []
    i = 0
    while i < len(arr) - 1:
        # If there's a row of at least two, start counting more
        if np.array_equal(arr[i:i + 2], [val, val]):
            # Initialize the sequence length to two
            seq += [2]
            end_val = len(arr)
            seq_index = len(seq) - 1

            # See if sequence is longer than two
            for j in range(i + 2, len(arr)):
                # Increment the sequence length if it's continued
                if arr[j] == val:
                    seq[seq_index] += 1
                # If the sequence is broken:
                else:
                    # The index of the last item in the sequence
                    end_val = j - 1
                    # Only save the sequence if it has a 0 on either side of it
                    if arr[j] == 0 or arr[i - 1] == 0:
                        seq[seq_index] = seq[seq_index]
                    else:
                        seq.pop()
                    break
            # If the sequence goes until the end of the array, remove it unless it has a 0 before it
            if end_val == len(arr) and arr[i - 1] != 0:
                seq.pop()
            # Set the for loop to start where the sequence ended
            i = end_val
        i += 1

    # Rounds  any value greater than 4 down to 4
    seq = [4 if val > 4 else val for val in seq]
    return seq


def is_game_won(board):
    lines = (
        board,  # row
        zip(*board),  # columns
        [np.diagonal(board, x) for x in range(-2, 4)],  # positive diagonals
        [np.diagonal(board[::-1], x) for x in range(-2, 4)]  # negative diagonals
    )

    for line in chain(*lines):
        for player_id, group in groupby(line):
            if player_id != 0 and len(list(group)) >= 4:
                return player_id
    return False
