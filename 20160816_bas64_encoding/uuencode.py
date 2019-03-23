import math
import bitarray
import sys


def encode_data(input_filename, output_filename):
    with open(input_filename, 'rb') as infile:
        data = infile.read()

    outfile = open(output_filename, 'w')

    # print header
    outfile.write("begin 644 %s\n" % input_filename)

    for lineOffset in range(0, len(data), 45):
        line_data = data[lineOffset:min(lineOffset+45, len(data))]
        # print length of encoded data
        outfile.write(chr(32 + len(line_data)))
        # encode and print data
        for y in range(0, len(line_data), 3):
            ba = bitarray.bitarray()
            sub_data = line_data[y:min(y+3, len(line_data))]
            ba.frombytes(sub_data + '0' * (3-len(sub_data)))
            bits = ba.tolist()
            if len(bits) < 24:
                bits = bits + [False] * (24 - len(bits))
            for x in range(0, len(bits), 6):
                hex_sum = 0
                for z in range(0, 6):
                    hex_sum = hex_sum * 2 + bits[x+z]
                hex_sum += 32
                outfile.write(chr(hex_sum))
        # end line
        outfile.write("\n")

    # print footer
    outfile.write("`\nend\n")

    outfile.close()

    print "Done encoding!"


def decode_data(input_filename):
    with open(input_filename, 'r') as infile:
        data = infile.read().split('\n')

    # parse header
    output_filename = data[0].split(' ')[2]
    outfile = open(output_filename, 'wb')

    # parse each line
    for line in data[1:]:
        if line == "end":
            break
        line_bytes = ord(line[0]) - 32
        line = line[1:]
        if line_bytes == 64:
            continue
        if 4 * math.ceil(line_bytes/3.0) != len(line):
            print "Incorrect byte length for: %s" % line
            break
        for i in range(0, len(line), 4):
            sub_line = line[i:min(len(line), i+4)]
            sub_ords = [ord(x) - 32 for x in sub_line]
            decoded_sub = ""
            decoded_sub += chr((sub_ords[0] << 2) % 256 + (sub_ords[1] >> 4))
            decoded_sub += chr((sub_ords[1] << 4) % 256 + (sub_ords[2] >> 2))
            decoded_sub += chr((sub_ords[2] << 6) % 256 + sub_ords[3])
            outfile.write(decoded_sub[0:min(3, line_bytes - 3*i/4)])
            sys.stdout.write(decoded_sub[0:min(3, line_bytes - 3*i/4)])

    outfile.close()

    print "Done decoding!"
