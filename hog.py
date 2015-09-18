"""This is a minimal contest submission file. You may also submit the full
hog.py from Project 1 as your contest entry.
"""
import collections
from random import randint
from scipy.special import comb

x5 = 1


def make_fair_dice(sides):
    """Return a die that returns 1 to SIDES with equal chance."""
    assert type(sides) == int and sides >= 1, 'Illegal value for sides'

    def dice():
        return randint(1, sides)

    return dice


four_sided = make_fair_dice(4)
six_sided = make_fair_dice(6)


def get_primes():
    """

    :return:
    >>> get_primes()[:3]
    [2, 3, 5]
    """
    global primes
    if primes is None:
        with open("primes1000.txt") as file:
            primes = list(map(int, file.readlines()))
    return primes


def is_prime(n):
    """

    :param n:
    :return:
    >>> is_prime(5)
    True
    >>> is_prime(1)
    False
    >>> is_prime(2)
    True
    >>> is_prime(39)
    False
    """
    return n in get_primes()


def previous_prime(n):
    """

    :param n:
    :return:
    >>> previous_prime(3)
    2
    >>> previous_prime(5)
    3
    """
    i = get_primes().index(n)
    if i == 0:
        return None
    else:
        return get_primes()[i - 1]


def next_prime(x):
    """

    :param x:
    :return:
    >>> next_prime(2)
    3
    >>> next_prime(3)
    5
    >>> next_prime(5)
    7
    >>> next_prime(7)
    11
    >>> next_prime(4)
    Traceback (most recent call last):
      ...
    AssertionError
    """
    assert type(x) == int
    assert is_prime(x)
    i = get_primes().index(x)
    return get_primes()[i + 1]


def is_win(score, opponent_score, goal=100):
    """

    :param score:
    :param opponent_score:
    :param goal:
    :return:
    >>> is_loss(100, 100)
    Traceback (most recent call last):
      ...
    AssertionError
    >>> is_win(100, 0)
    True
    >>> is_win(50, 50)
    False
    >>> is_win(0, 100)
    False
    """
    assert not (score >= goal and opponent_score >= goal)
    return score >= goal > opponent_score


def is_loss(score, opponent_score, goal=100):
    """

    :param score:
    :param opponent_score:
    :param goal:
    :return:
    >>> is_loss(100, 100)
    Traceback (most recent call last):
      ...
    AssertionError
    >>> is_loss(100, 0)
    False
    >>> is_loss(50, 50)
    False
    >>> is_loss(0, 100)
    True
    """
    assert not (score >= goal and opponent_score >= goal)
    return is_win(opponent_score, score, goal)


def free_bacon(opponent_score):
    """
    Another custom rule from the game of hog.
    :param opponent_score:
    :return: One more than the greatest digit in opponent_score
    >>> free_bacon(67)
    8
    >>> free_bacon(0)
    1
    >>> free_bacon(123)
    4
    """
    return max(map(int, str(opponent_score))) + 1


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    >>> select_dice(7, 0) == four_sided
    True
    >>> select_dice(8, 0) == six_sided
    True
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    >>> is_swap(19, 91)
    True
    >>> is_swap(9, 90)
    True
    >>> is_swap(90, 9)
    True
    >>> is_swap(1, 1)
    False
    """
    # BEGIN Question 4
    a = score0 % 100  # last two digits of score0
    b1 = score1 % 10  # last digit of score1
    b2 = score1 % 100 // 10  # second to last digit of score1
    return a == b1 * 10 + b2
    # END Question 4


def hogtimus_prime(turn_score):
    """

    :param turn_score:
    :return:
    >>> hogtimus_prime(4)
    4
    >>> hogtimus_prime(2)
    3
    """
    if is_prime(turn_score):
        return next_prime(turn_score)
    return turn_score


def score_tree(n, dice, opponent_score):
    """


    :param opponent_score:
    :param n:
    :return:
    >>> score_tree(3,four_sided, 95)
    """
    if n == 0:
        return {free_bacon(opponent_score): 1}
    if dice == six_sided:
        sides = 6
    else:
        sides = 4

    score_map = collections.defaultdict(lambda: 0)
    score_map[0] = prob_rolling_1(n, sides)
    for p in range(n * 2, n * sides + 1):
        if p == 2:
            score_map[p] = 0  # 2 is the first prime, so there's no way we can score 2
        elif is_prime(p):
            next_p = next_prime(p)
            score_map[next_p] = get_probability(p, n, sides)
        else:
            score_map[p] = get_probability(p, n, sides)

    return score_map


def prob_rolling_1(n, sides):
    """

    :param n:
    :param sides:
    :return:
    >>> prob_rolling_1(1, 4)
    0.25
    >>> prob_rolling_1(2, 4)
    0.4375
    """
    return 1 - (((sides - 1) / sides) ** n)


def ncr(n, r):
    """

    :param n:
    :param r:
    :return:
    >>> ncr(12, 5)
    792
    >>> ncr(10, 7)
    120
    >>> ncr(8, 3)
    56
    """
    return comb(n, r, exact=True)


def probability_parse(line):
    line_split = line.split(",")
    return tuple(map(int, line_split[:3])), float(line_split[3])


def get_probability(p, n, s):
    return ((s - 1) / s) ** n * get_probability_normal_dice(p - n, n, s - 1)


def get_probability_normal_dice(p, n, s):
    """

    :param p: sum
    :param n: num rolls
    :param s: num sides
    :return:
    >>> get_probability_normal_dice(7, 2, 6)
    0.16666666666666666
    """
    return 1 / s ** n * sum([(-1) ** k * ncr(n, k) * ncr(p - s * k - 1, n - 1) for k in range(0, int((p - n) / s) + 1)])


def get_best_chances_dict(against):
    global best_chances_dict
    file_name = get_file_name(against)
    if best_chances_dict is None:
        with open(file_name, "r") as file:
            lines = file.readlines()
            best_chances_dict = dict(parse(line) for line in lines)
    return best_chances_dict


def get_outcome_map(n, score, opponent_score):
    """

    :param n:
    :param score:
    :param opponent_score:
    :return:
    """
    score_map = score_tree(n, select_dice(score, opponent_score), opponent_score)
    if len(score_map) == 1:
        turn_score = next(iter(score_map.keys()))
        new_score, new_opponent_score = score, opponent_score
        if turn_score == 0:
            new_opponent_score += n
        else:
            new_score += turn_score
        if is_swap(new_score, new_opponent_score):
            new_score, new_opponent_score = new_opponent_score, new_score
        return {(new_score, new_opponent_score): 1.0}

    outcome_map = collections.defaultdict(lambda: 0)
    for turn_score in score_map:
        new_score, new_opponent_score = score, opponent_score
        if turn_score == 0:
            new_opponent_score += n
        else:
            new_score += turn_score
        if is_swap(new_score, new_opponent_score):
            new_score, new_opponent_score = new_opponent_score, new_score
        outcome_map[(new_score, new_opponent_score)] += score_map[turn_score]
    return outcome_map


def throws(f, *args):
    try:
        f(*args)
    except:
        return True
    return False


def get_file_name(against):
    if against == x5:
        return "x5.txt"


def get_best_move(score, opponent_score, against):
    """

    :param score:
    :param opponent_score:
    :return:
    >>> get_best_move(99, 99)
    (0, 1.0)
    >>> get_best_move(90, 99)
    (0, 1.0)
    """
    if (score, opponent_score) in get_best_chances_dict(against):
        return get_best_chances_dict()[(score, opponent_score)]
    best_n, best_chance = 0, 0
    for n in range(0, 11):
        outcome_chance = get_outcome_chance(score, opponent_score, n, against)

        if outcome_chance > best_chance:
            best_n, best_chance = n, outcome_chance

    file_name = get_file_name(against)
    with open(file_name, "a") as file:
        get_best_chances_dict(against)[(score, opponent_score)] = (best_n, best_chance)
        file.write("%d,%d,%d,%f\n" % (score, opponent_score, best_n, best_chance))
    return best_n, best_chance


def get_outcome_chance(score, opponent_score, n, against):
    outcome_map = get_outcome_map(n, score, opponent_score)
    outcome_chance = 0
    for outcome in outcome_map:
        count = outcome_map[outcome]
        if is_win(outcome[0], outcome[1]):
            outcome_chance += count * 1.0
        elif is_loss(outcome[0], outcome[1]):
            outcome_chance += count * 0.0  # should just be pass
        else:
            if against == final_strategy:
                outcome_chance += count * (1 - get_best_move(outcome[1], outcome[0])[1])
            else:
                sub_outcome_chance = 0
                sub_outcome_map = get_outcome_map(5, outcome[1], outcome[0])
                for sub_outcome in sub_outcome_map:
                    sub_count = sub_outcome_map[sub_outcome]
                    if is_win(sub_outcome[1], sub_outcome[0]):
                        sub_outcome_chance += sub_count * 1.0
                    elif is_loss(sub_outcome[1], sub_outcome[0]):
                        sub_outcome_chance += sub_count * 0.0
                    else:
                        sub_outcome_chance += sub_count * get_best_move(sub_outcome[1], sub_outcome[0])[1]
                outcome_chance += count * sub_outcome_chance
    return outcome_chance


def parse(line):
    line_split = line.split(",")
    return (int(line_split[0]), int(line_split[1])), (int(line_split[2]), float(line_split[3]))


def final_strategy(score, opponent_score, against=x5):
    return get_best_move(score, opponent_score, against)[0]


def generate_strategy():
    """

    :return:
    """
    score = 99
    while score >= 0:
        opp = 99
        while opp >= 0:
            final_strategy(score, opp)
            opp -= 1
        score -= 1
