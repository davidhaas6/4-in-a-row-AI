from itertools import chain, groupby


def contains(parent_list, sub_list):
    """See if a list contains the exact sequence of a sublist"""
    for i in range(len(parent_list) - len(sub_list) + 1):
        print parent_list[i:i + len(sub_list)]
        if parent_list[i:i + len(sub_list)] == sub_list:
            return True
    return False


def get_major_diagonals(arr2d, x_range, y_range):
    """
    Returns major diagonals (they go like this: \)
    @:param: x_range The number columns to the right (of arr[0][0]) to get the diagonals of
    @:param: y_range The number of rows down (from arr[0][0]) to get the diagonals of
    """
    rows, columns = 6, 7

    diagonals = [[arr2d[r + y_offset][r] for r in range(rows - y_offset)] for y_offset in range(y_range, -1, -1)]
    diagonals += [[arr2d[r][r + x_offset] for r in range(rows - (x_offset - 1))] for x_offset in range(1, x_range + 1)]
    '''
    # DECOMPRESSED VERSION OF THE TWO ABOVE LINES:
    for y_offset in range(y_range, -1, -1):
        for r in range(rows - y_offset):
            temp_diag += [arr2d[r + y_offset][r]]
        diagonals += [temp_diag]
        temp_diag = []
    for x_offset in range(1, x_range + 1):
        for r in range(rows - (x_offset - 1)):
            temp_diag += [arr2d[r][r + x_offset]]
        diagonals += [temp_diag]
        temp_diag = []
    '''
    return diagonals


def get_minor_diagonals(arr2d, x_range, y_range):
    """
    Returns major diagonals (they go like this: /)
    @:param: x_range The number columns to the right (of bottom left) to get the diagonals of
    @:param: y_range The number of rows up (from bottom left) to get the diagonals of
    """
    return get_major_diagonals(arr2d[::-1], x_range, y_range)


def sequences(arr, val):
    """Returns array of sequence lengths of a value in an array"""
    # TODO: OPTIMIZE!!!!!!!
    # TODO: Make it so 1, 1, 0, 1 counts as 3-row??
    # List of lengths of sequences
    seq = []
    i = 0
    array_length = len(arr)  # Saved as variable to reduce len() calls
    while i < array_length - 1:
        # If there's a row of at least two, start counting more
        if arr[i] == arr[i + 1] == val:
            # Initialize the sequence length to two
            seq += [2]
            end_val = array_length
            seq_index = len(seq) - 1

            # See if sequence is longer than two
            for j in range(i + 2, array_length):
                # Increment the sequence length if it's continued
                if arr[j] == val:
                    seq[seq_index] += 1
                # If the sequence is broken:
                else:
                    # The index of the last item in the sequence
                    end_val = j - 1
                    # Only save the sequence if it has a 0 on either side of it and sequence is in middle
                    if i > 0:
                        if not (arr[j] == 0 or arr[i - 1] == 0) and seq[seq_index] < 4:
                            seq.pop()
                    # If the sequence starts at the first column, only save if it has a 0 after it
                    elif i == 0:
                        if arr[j] != 0 and seq[seq_index] < 4:
                            seq.pop()
                    break
            # If the sequence goes until the end of the array, remove it unless it has a 0 before it
            if end_val == array_length and arr[i - 1] != 0 and seq[seq_index] < 4:
                seq.pop()
            # Set the for loop to start where the sequence ended
            i = end_val
        i += 1

    # Rounds  any value greater than 4 down to 4
    seq = [4 if val > 4 else val for val in seq]
    return seq


def get_sequence(arr, val, index, array_length):
    # Initialize the sequence length to two
    sequence_length = 2
    end_val = array_length

    # See if sequence is longer than two
    for j in range(index + 2, array_length):
        # Increment the sequence length if it's continued
        if arr[j] == val:
            sequence_length += 1
        # If the sequence is broken:
        else:
            # The index of the last item in the sequence
            end_val = j - 1
            # Only save the sequence if it has a 0 on either side of it and sequence is in middle of row
            if index > 0:
                if not (arr[j] == 0 or arr[index - 1] == 0) and sequence_length < 4:
                    sequence_length = -1
            # If the sequence starts at the first column, only save if it has a 0 after it
            elif index == 0:
                if arr[j] != 0 and sequence_length < 4:
                    sequence_length = -1
            break
    # If the sequence goes until the end of the array, remove it unless it has a 0 before it
    if end_val == array_length and arr[index - 1] != 0 and sequence_length < 4:
        sequence_length = -1
    # Set the for loop to start where the sequence ended
    return end_val, sequence_length


def sequences_of_each(arr, val1=1, val2=2):
    """Returns array of sequence lengths of a value in an array"""
    # TODO: OPTIMIZE!!!!!!!
    # TODO: Make it so 1, 1, 0, 1 counts as 3-row??
    # List of lengths of sequences
    seq1 = []
    seq2 = []
    i = 0
    array_length = len(arr)  # Saved as variable to reduce len() calls
    while i < array_length - 1:
        # If there's a row of at least two, start counting more
        if arr[i] == arr[i + 1] == val1:
            f = get_sequence(arr, val1, i, array_length)
            i = f[0]
            if f[1] != -1:
                seq1 += [f[1]]
        elif arr[i] == arr[i + 1] == val2:
            f = get_sequence(arr, val2, i, array_length)
            i = f[0]
            if f[1] != -1:
                seq2 += [f[1]]
        i += 1

    # Rounds  any value greater than 4 down to 4
    seq1 = [4 if val > 4 else val for val in seq1]
    seq2 = [4 if val > 4 else val for val in seq2]
    return [seq1, seq2]


def seq_short(board_orientations):
    # TODO: Needs to omit sequence if it has no 0s on either end.
    seq = [[], []]
    for row in chain(*board_orientations):
        groups = [(g[0], len(list(g[1]))) for g in groupby(row)]
        num_groups = len(groups)
        for i in range(num_groups):
            player_id, sequence_length = groups[i]
            if player_id != 0 and sequence_length >= 2:
                # Sorry for multiple if statements!.. couldn't think of any cleaner way to write it

                # If it starts at beginning, check if followed by a 0 (empty space)
                if i == 0 and groups[i + 1][0] == 0:
                    seq[player_id - 1] += [sequence_length]
                # If it's in the middle, check if a 0 is on either side
                elif (0 < i < num_groups - 1) and (groups[i + 1][0] == 0 or groups[i - 1][0] == 0):
                    seq[player_id - 1] += [sequence_length]
                # If it's at the end, check if it's 4 in a row, or has a 0 before it
                elif i == num_groups - 1 and (groups[i - 1][0] == 0 or sequence_length >= 4):
                    seq[player_id - 1] += [sequence_length]
    return seq


def is_game_won(board_orientations):
    # Every possible orientation of the board

    for line in chain(*board_orientations):
        for player_id, group in groupby(line):
            if player_id != 0 and len(list(group)) >= 4:
                return player_id
    return False
