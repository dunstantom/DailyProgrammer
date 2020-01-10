import string
import numpy as np
import re


def get_morse_dict():
    morse_alphabet_str = ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --.."
    return dict(zip(string.ascii_lowercase, morse_alphabet_str.split()))


def smorse(s):
    morse_dict = get_morse_dict()
    return "".join([morse_dict[c] for c in s])


def is_balanced_smorse(s):
    only_dots = [c for c in s if c == '.']
    return 2*len(only_dots) == len(s)


def is_palindrome(s):
    return s == s[::-1]


smorse_to_binary_trans = str.maketrans(".-", "01")
binary_to_smorse_trans = str.maketrans("01", ".-")


def smorse_to_binary(s):
    return s.translate(smorse_to_binary_trans)


def binary_to_smorse(x):
    binary_str = "{:013b}".format(x)
    return binary_str.translate(binary_to_smorse_trans)


def find_all_sequences(s):
    binary_s = smorse_to_binary(s)
    found_ints = []
    if len(s) >= 13:
        for i in range(0, len(s)-12):
            found_ints.append(int(binary_s[i:i+13], base=2))
    return found_ints


def main():
    word_translation = {}
    for line in open('enable1.txt', 'r'):
        word = line.strip()
        if len(word) > 0:
            word_translation[word] = smorse(word)

    # Bonus 1: find only sequence that is code for 13 words
    values, counts = np.unique(list(word_translation.values()), return_counts=True)
    bonus_1_ans = values[counts == 13]
    print(f"Bonus 1: sequence for 13 words => {bonus_1_ans}")
    print("Words with this sequence:")
    bonus_1_words = [key for key, val in word_translation.items() if val == bonus_1_ans]
    for word in bonus_1_words:
        print(word)

    # Bonus 2: Find only word that has 15 dashes in a row
    fifteen_dashes = re.compile("\-{15}")
    bonus_2_ans = [key for key, val in word_translation.items() if fifteen_dashes.search(val) is not None][0]
    print(f"Bonus 2: only word with 15 dashes in a row => {bonus_2_ans}")
    print(f"    smorse() => {word_translation[bonus_2_ans]}")

    # Bonus 3: "balanced" = same # of dots and dashes, find two 21-letter balanced words
    bonus_3_ans = [key for key, val in word_translation.items() if (len(key) == 21) & is_balanced_smorse(val)]
    print(f"Bonus 3: 21-letter words with balanced smorse: {bonus_3_ans}")

    # Bonus 4: Find only 13-letter word that encodes to a palindrome
    bonus_4_ans = [k for k,v in word_translation.items() if (len(k) == 13) & is_palindrome(v)][0]
    print(f"Bonus 4: 13-letter word that encodes to palindrome: {bonus_4_ans} => {word_translation[bonus_4_ans]}")

    # Bonus 5: Find the five 13-char sequences that don't appear in any encoding
    # 13-char sequence => 8192 patterns
    sequence_dict = {i: 0 for i in range(0, 8192)}
    for k, v in word_translation.items():
        sequence_ints = find_all_sequences(v)
        sequence_dict.update(dict.fromkeys(sequence_ints, 1))

    bonus_5_ans = [binary_to_smorse(k) for k, v in sequence_dict.items() if v == 0]
    print("Bonus 5: 13-char sequences that don't appear in any encoding:")
    print("\n".join(bonus_5_ans))


if __name__ == "__main__":
    main()
