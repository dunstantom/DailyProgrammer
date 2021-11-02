import itertools
from os.path import exists
import urllib.request
from collections import Counter


def letter_sum(input_string):
    total = 0
    for c in input_string:
        total = total + ord(c) - 96  # ord('a') == 97
    return total


def main():
    res = letter_sum("microspectrophotometries")
    print(f"letter_sum(\"microspectrophotometries\") => {res}")
    print("")

    print("Loading and scoring words...")
    with open("enable1.txt", "r") as f:
        words = [x.strip() for x in f.readlines()]

    words_scored = [(w, letter_sum(w)) for w in words]

    print("Bonus challenge 1:")
    words_319 = [w for (w, score) in words_scored if score == 319]
    print(f"Word(s) with a sum of 319: {words_319}\n")

    print("Bonus challenge 2:")
    words_odd = [w for (w, score) in words_scored if score % 2 == 1]
    print(f"Word(s) with an odd sum: {len(words_odd)}\n")

    print("Bonus challenge 3:")
    score_counts = Counter([s for (_, s) in words_scored])
    (top_score, score_freq) = score_counts.most_common(1)[0]
    print(f"Most common sum, {top_score}, occurred {score_freq} times.\n")

    print("Bonus challenge 4:")
    for k, g in itertools.groupby(sorted(words_scored, key=lambda x: x[1]), lambda x: x[1]):
        if (k == 151) or (k == 219):  # to speed up reprocessing
            for w1, w2 in itertools.combinations(g, 2):
                len_diff = abs(len(w1[0]) - len(w2[0]))
                if len_diff == 11:
                    print(f"{w1}, {w2} have score {k} and differ by {len_diff} in length")
    print("")

    print("Bonus challenge 5:")
    for k, g in itertools.groupby(sorted(words_scored, key=lambda x: x[1]), lambda x: x[1]):
        if k > 188:
            for w1, w2 in itertools.combinations(g, 2):
                s1 = set(w1[0])
                s2 = set(w2[0])
                if len(set(w1[0] + w2[0])) == (len(s1) + len(s2)):
                    print(f"{w1}, {w2} have score {k} and no characters in common")
    print("")

    print("Bonus challenge 6:")
    words_stats = [(w, s, len(w)) for (w, s) in words_scored]
    unique_stats = set([(s, l) for (w, s, l) in words_stats])
    word_list = []

    def find_min_stat(min_letter_sum=None):
        if letter_sum is None:
            sum_counts = Counter([s for (s, _) in unique_stats])
            return sum_counts.most_common()[-1][0]
        else:
            min_lens = set([l for (s, l) in unique_stats if s == min_letter_sum])
            len_counts = Counter([l for (_, l) in unique_stats if l in min_lens])
            return len_counts.most_common()[-1][0]

    while len(unique_stats) > 0:
        # find letter sum with min number of tuples
        min_sum = find_min_stat()
        # find lengths associated with min letter sum with min number of tuples
        min_len = find_min_stat(min_sum)
        # add a word with this letter sum and length to word list
        word_list = word_list + [[(w, s, l) for (w, s, l) in words_stats if (s == min_sum) and (l == min_len)][0]]
        # remove all stat entries with either letter sum or length
        unique_stats = unique_stats - set([(s, l) for (s, l) in unique_stats if s == min_sum or l == min_len])

    word_list = sorted(sorted(word_list, key=lambda x: x[2]), key=lambda x: -x[1])
    for (w, s, l) in word_list:
        print(w, s, l)
    print("List length: " + str(len(word_list)))
    print("Done!")


if __name__ == "__main__":
    if not exists("enable1.txt"):
        urllib.request.urlretrieve("https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt",
                                   "enable1.txt")
    main()
