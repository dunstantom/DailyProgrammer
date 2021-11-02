import main


def test_letter_sum():
    tests = [("", 0), ("a", 1), ("z", 26), ("cab", 6), ("excellent", 100), ("microspectrophotometries", 317)]
    for (input_string, expected_sum) in tests:
        assert main.letter_sum(input_string) == expected_sum
