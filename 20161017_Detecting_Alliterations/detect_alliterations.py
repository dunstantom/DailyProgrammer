# Reddit DailyProgrammer challenge link:
# https://www.reddit.com/r/dailyprogrammer/comments/57zcbm/20161017_challenge_288_easy_detecting_alliteration/
# Note: The sample outputs are not consistent (as discussed in the comments), so this is an 'interpretive' solution.
import io
import string


def strip_punctuation(s):
    return ''.join(ch for ch in s if ch not in set(string.punctuation))


def main(input_filename, stopwords_filename):
    with io.open(stopwords_filename, 'r') as stopwords_file:
        stopwords = stopwords_file.read().split('\n')

    with io.open(input_filename, 'r') as input_file:
        num_lines = int(input_file.readline())
        lines = input_file.read().split('\n')
        assert len(lines) == num_lines

    for line in lines:
        line = [word for word in strip_punctuation(line.lower()).split(' ') if word not in stopwords]
        alliterations = []
        while line:
            next_alliteration = [word for word in line if word[0] == line[0][0]]
            line = [word for word in line if word[0] != line[0][0]]
            if len(next_alliteration) > 1:
                alliterations.append(' '.join(next_alliteration))
        print '\t'.join(alliterations)


if __name__ == "__main__":
    main("input.txt", "stopwords.txt")
