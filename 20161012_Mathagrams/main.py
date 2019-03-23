# Brute-force approach: solved the challenges as below:
# Solution (in 20 steps): 273 + 681 = 954
# Solution (in 14 steps): 273 + 591 = 864
# Solution (in 43 steps): 281 + 394 = 675
from copy import copy


def brute_force(terms, candidates):
    global solutions_attempted
    unsolved = [i for (i, x) in enumerate(terms) if x == 'x']
    if not unsolved:
        solutions_attempted += 1
        term1 = ''.join(terms[:3])
        term2 = ''.join(terms[3:6])
        term3 = ''.join(terms[6:])
        if int(term1) + int(term2) == int(term3):
            return '%s + %s = %s' % (term1, term2, term3)
        else:
            return None

    solve_for = unsolved[0]
    for c in candidates:
        terms[solve_for] = str(c)
        next_candidates = copy(candidates)
        next_candidates.remove(c)
        a = brute_force(copy(terms), next_candidates)
        terms[solve_for] = 'x'
        if a:
            return a
    return None


def solve_mathagram(q):
    global solutions_attempted
    solutions_attempted = 0
    parts = [p for p in q.split(' ') if p != "+" and p != "="]
    assert len(parts) == 3
    terms = list(''.join(parts))
    candidates = [i for i in range(1, 10) if str(i) not in terms]
    return brute_force(terms, candidates)


if __name__ == "__main__":
    q = "xxx + x81 = 9x4"
    a = solve_mathagram(q)
    print 'Solution (in %d steps): %s' % (solutions_attempted, a)

    q = "xxx + 5x1 = 86x"
    a = solve_mathagram(q)
    print 'Solution (in %d steps): %s' % (solutions_attempted, a)

    q = "xxx + 39x = x75"
    a = solve_mathagram(q)
    print 'Solution (in %d steps): %s' % (solutions_attempted, a)
