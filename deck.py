import random
from tripeaks import Game
from basic_operations import *


def generate_hands(num):
    hand = [
        '{}{}'.format(rank, suit) for suit in ('c', 'd', 'h', 's') for rank in list(range(2, 11)) + ['J', 'Q', 'K', 'A']
    ]
    for n in range(num):
        print('#' + str(n))
        if n > 30:
            random.shuffle(hand)
            yield hand[: 24], hand[24:]


@which_watch
def experiment(num):
    res = list()
    for pile, seq in generate_hands(num):
        start = time.time()
        won = Game(seq, pile).play()
        fin = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
        print(fin + '\n')
        res.append((won, fin))
    for won, timing in res:
        print(won, timing)


if __name__ == '__main__':
    random.seed(0)
    experiment(50)
