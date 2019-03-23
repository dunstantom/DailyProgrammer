import sys
from math import log10, floor, pow


def main():
    if len(sys.argv) < 2:
        print "error: no arguments provided"

    for arg in sys.argv[1:]:
        # for each number, print number plus one to each digit
        print(arg, increment_digits(int(arg)))


def increment_digits(x):
    if x < 10:
        return x+1
    return increment_digits(floor(x / 10.0)) * 10 + (x % 10) + 1
    # max_digit_pos = floor(log10(x))  # 0-base
    # mask = pow(10, max_digit_pos)
    # digit = floor(x / mask)
    # remain = x % mask
    # i_d = (digit + 1) * mask
    # new_x = i_d + incr_digits(remain)
    # return int(new_x)


if __name__ == "__main__":
    main()
