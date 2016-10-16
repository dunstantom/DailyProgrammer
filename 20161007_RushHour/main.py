# Reddit DailyProgrammer Challenge:
# https://www.reddit.com/r/dailyprogrammer/comments/56bh88/20161007_challenge_286_hard_rush_hour_solver/
import sys
import io
from collections import namedtuple

Location = namedtuple('Location', ['r', 'c'])


class Vehicle:
    def __init__(self, name='', is_car=True, is_horizontal=True, loc=Location(0, 0)):
        self.name = name
        self.isCar = is_car
        self.isHorizontal = is_horizontal
        self.location = loc

    def length(self):
        return 2 + (not self.isCar)

    def right_col(self):
        return self.location.c + self.isHorizontal * (self.length() - 1)

    def bottom_row(self):
        return self.location.r + (not self.isHorizontal) * (self.length() - 1)

    def move_car(self, direction):
        if (self.isHorizontal and direction.r != 0) or (not self.isHorizontal and direction.c != 0):
            raise Exception("Trying to move car against direction")
        self.location = Location(self.location.r + direction.r, self.location.c + direction.c)

    def occupies(self, space):
        if self.isHorizontal:
            return (self.location.r == space.r) and space.c in range(self.location.c, self.location.c + self.length())
        else:
            return (self.location.c == space.c) and space.r in range(self.location.r, self.location.r + self.length())

    def move_out(self, space, board_limits):
        if self.isHorizontal:
            move_right = Location(0, space.c - self.location.c + 1)
            move_left = Location(0, space.c - self.location.c - self.length())
            if self.location.c + move_left.c < 0:
                move_left = None
            if self.location.c + self.length() - 1 + move_right.c >= board_limits.c:
                move_right = None
            return move_left, move_right
        else:
            move_down = Location(space.r - self.location.r + 1, 0)
            move_up = Location(space.r - self.location.r - self.length(), 0)
            if self.location.r + move_up.r < 0:
                move_up = None
            if self.location.r + self.length() - 1 + move_down.r >= board_limits.r:
                move_down = None
            return move_up, move_down


class Board:
    def __init__(self, file_name):
        with io.open(file_name, 'r') as input_file:
            board_data = input_file.read().split('\n')
        self.vehicles = dict()
        self.num_rows = len(board_data)
        self.num_cols = min([len(x) for x in board_data])
        self.goal_row = [i for i in range(0, len(board_data)) if board_data[i][-1] == '>'][0]
        board_data[self.goal_row] = board_data[self.goal_row][:-1]

        for r in range(0, len(board_data)):
            for c in range(0, len(board_data[r])):
                if board_data[r][c] != '.' and board_data[r][c] not in self.vehicles:
                    self.vehicles[board_data[r][c]] = self.get_vehicle(board_data, Location(r, c))

    @staticmethod
    def get_vehicle(board_data, loc):
        name = board_data[loc.r][loc.c]
        if loc.r != (len(board_data) - 1) and board_data[loc.r+1][loc.c] == name:
            is_horizontal = False
            if loc.r + 2 < len(board_data) and board_data[loc.r + 2][loc.c] == name:
                is_car = False
            else:
                is_car = True
        else:
            is_horizontal = True
            if loc.c + 2 < len(board_data[loc.r]) and board_data[loc.r][loc.c + 2] == name:
                is_car = False
            else:
                is_car = True
        return Vehicle(name, is_car, is_horizontal, loc)

    def solve_board(self):
        while not self.solved():
            if not self.move_car('R', Location(0, 1), []):
                print "Failed to move R from (%d, %d)" % (self.vehicles['R'].location.r, self.vehicles['R'].location.c)
                return
        print "Solved!"

    def solved(self):
        return self.vehicles['R'].right_col() == self.num_cols - 1

    def move_car(self, car_name, direction, car_queue):
        move_horizontal = (direction.r == 0)
        for i in range(0, max(abs(direction.r), abs(direction.c))):
            if move_horizontal:
                next_step = Location(0, 1 - (direction.c < 0) * 2)
            else:
                next_step = Location(1 - (direction.r < 0) * 2, 0)
            # if this move is already on the queue, then we have circular dependency and need to bail
            if (car_name, next_step) in car_queue:
                return False
            car_queue.append((car_name, next_step))
            # find if space is blocked and, if so, what's blocking
            blocker, unblock_direction_1, unblock_direction_2 = self.find_blocking_car(car_name, next_step)
            # while space is blocked, move cars
            while blocker is not None:
                if unblock_direction_1 is None or not self.move_car(blocker, unblock_direction_1, car_queue):
                    if unblock_direction_2 is None or not self.move_car(blocker, unblock_direction_2, car_queue):
                        return False
                blocker, unblock_direction_1, unblock_direction_2 = self.find_blocking_car(car_name, next_step)
            # if blocker moved, move car
            self.vehicles[car_name].move_car(next_step)
            q_car_name, q_dir = car_queue.pop()
            print 'Moved: %s (%d, %d)' % (q_car_name, q_dir.r, q_dir.c)
        return True

    def find_blocking_car(self, car_name, direction):
        next_space = Location(
            self.vehicles[car_name].location.r + direction.r + (direction.r > 0) *
            (self.vehicles[car_name].length() - 1),
            self.vehicles[car_name].location.c + direction.c + (direction.c > 0) *
            (self.vehicles[car_name].length() - 1)
        )
        blockers = [c for c in self.vehicles.values() if c.occupies(next_space)]
        if not blockers:
            return None, None, None
        else:
            blocker = blockers[0]
            direction_1, direction_2 = blocker.move_out(next_space, Location(self.num_rows, self.num_cols))
            return blocker.name, direction_1, direction_2


def main(input_filename):
    board_data = Board(input_filename)
    board_data.solve_board()
    print 'Done'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Bad arguments. Usage: main.py <input file>")
    main(sys.argv[1])
