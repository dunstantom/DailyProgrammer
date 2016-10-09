import sys
import io


def main(input_filename):
    board_data = read_board_data(input_filename)

    for line in board_data:
        print line

    solve_board(board_data)


def read_board_data(input_filename):
    with io.open(input_filename, 'r') as inpput_file:
        board_data = inpput_file.read().split('\n')
    return board_data


def solve_board(board_data):
    while not solved(board_data):
        board_data = move_car(board_data, 'R', (0, 1))
    print "Solved!"


def solved(board_data):
    return any([x[-1] == 'R' for x in board_data])


def move_car(board_data, car_name, direction):
    blocker = find_blocking_car(board_data, car_name, direction)
    updated_board = board_data
    if blocker is not None:
        updated_board = unblock_car(board_data, car_name, direction, blocker)
    updated_board = update_board(updated_board, car_name, direction)

    return updated_board


def unblock_car(board_data, car_name, direction, blocker):
    blocker_car = board_data[blocker[0]][blocker[1]]
    updated_board = board_data

    if direction[0] != 0:
        # need to move blocker left/right
        left_spaces = sum([1 for x in board_data[blocker[0]][blocker[1]:] if x == blocker_car])
        right_spaces = sum([1 for x in board_data[blocker[0]][:blocker[1]+1] if x == blocker_car])
        # try left
        for i in range(0, left_spaces):
            if updated_board is None:
                break
            updated_board = move_car(updated_board, blocker_car, (0, -1))
        # if not, try right
        if updated_board is not None:
            return updated_board
        updated_board = board_data
        for i in range(0, right_spaces):
            if updated_board is None:
                break
            updated_board = move_car(updated_board, blocker_car, (0, 1))
    else:
        # need to move blocker up/down
        up_spaces = sum([1 for x in board_data[blocker[0]][blocker[1]:] if x == blocker_car])
        down_spaces = sum([1 for x in board_data[blocker[0]][:blocker[1] + 1] if x == blocker_car])
        # try up
        for i in range(0, up_spaces):
            if updated_board is None:
                break
            updated_board = move_car(updated_board, blocker_car, (-1, 0))
        # if not, try down
        if updated_board is not None:
            return updated_board
        for i in range(0, down_spaces):
            if updated_board is None:
                break
            updated_board = move_car(updated_board, blocker_car, (1, 0))

    return updated_board


def update_board(board_data, car_name, direction):
    search_forward = True  # default to looking for left/top edge of car
    if direction[0] > 0 or direction[1] > 0:
        search_forward = False  # if we're moving down/right, we want to find bottom/right edge of car
    start = 0 if search_forward else len(board_data) - 1
    end = len(board_data) if search_forward else -1
    step = 1 if search_forward else -1
    for r in range(start, end, step):
        for c in range(start, end, step):
            if board_data[r][c] == car_name:
                board_data[r+direction[0]][c+direction[1]] = car_name
                if board_data[r-direction[0]*2][c-direction[1]*2] == car_name:
                    board_data[r - direction[0] * 2][c - direction[1] * 2] = '.'
                else:
                    board_data[r - direction[0]][c - direction[1]] = '.'
    return board_data


def find_blocking_car(board_data, car_name, direction):
    search_forward = True  # default to looking for left/top edge of car
    if direction[0] > 0 or direction[1] > 0:
        search_forward = False  # if we're moving down/right, we want to find bottom/right edge of car
    start = 0 if search_forward else len(board_data)-1
    end = len(board_data) if search_forward else -1
    step = 1 if search_forward else -1
    for r in range(start, end, step):
        for c in range(start, end, step):
            if board_data[r][c] == car_name:
                (x, y) = (r + direction[0], c + direction[1])
                if x < 0 or x >= len(board_data) or y < 0 or y >= len(board_data):
                    return None
                return x, y


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Bad arguments. Usage: main.py <input file>")
    main(sys.argv[1])
