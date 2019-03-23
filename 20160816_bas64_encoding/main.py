import sys
import uuencode


def main(args):
    if args[0] == "encode" and len(args) == 3:
        uuencode.encode_data(args[1], args[2])
    elif args[0] == "decode" and len(args) == 2:
        uuencode.decode_data(args[1])
    else:
        print "Command %s is not recognzied in %s" % (args[0], args)


if __name__ == "__main__":
    main(sys.argv[1:])
