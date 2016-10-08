import sys
import io


def main(input_filename):
    with io.open(input_filename, 'r') as inpput_file:
        board_data = inpput_file.read().split('\n')

    for line in board_data:
        print line

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Bad arguments. Usage: main.py <input file>")
    main(sys.argv[1])
