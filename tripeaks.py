import time
from copy import copy, deepcopy
from collections import deque


def which_watch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("\n{} took {}\n".format(func.__name__, time.strftime("%H:%M:%S", time.gmtime(time.time() - start))))
        return result

    return wrapper


class Card:
    def __init__(self, raw_card):
        self.mapper = {'J': 11, 'Q': 12, 'K': 13, 'A': 1}
        self.inv_mapper = {val: key for key, val in self.mapper.items()}
        self.readable = raw_card
        self.card = self.process_card()

    def __eq__(self, other):
        return self.readable == other.readable

    def __lt__(self, other):
        return self.readable < other.readable

    def __repr__(self):
        return "Card('{}')".format(self.readable)

    def __hash__(self):
        return hash(repr(self))

    def process_card(self):
        num = self.readable[: -1]
        return int(self.mapper.get(num, num)), self.readable[-1]

    def match(self, other):
        num, other_num = [card[0] for card in (self.card, other.card)]
        return abs(num - other_num) in (1, 12)


class Tableau:
    def __init__(self, seq):
        self.tableau = self.fill_in(seq)

    def __getitem__(self, item):
        return self.tableau[item]

    def __iter__(self):
        for parent in self.tableau:
            yield parent

    def __repr__(self):
        string = str()
        for parent in sorted(self.tableau.keys()):
            string += "{}: {}\n".format(parent.readable,
                                        ", ".join(sorted([child.readable for child in self.tableau[parent]])))
        return string

    def __len__(self):
        return len(self.tableau)

    def items(self):
        return self.tableau.items()

    @staticmethod
    def fill_in(seq):
        seq = [Card(card) for card in seq]
        tableau = {seq[0]: [seq[3], seq[4]],
                   seq[1]: [seq[5], seq[6]],
                   seq[2]: [seq[7], seq[8]],
                   seq[3]: [seq[9], seq[10]],
                   seq[4]: [seq[10], seq[11]],
                   seq[5]: [seq[12], seq[13]],
                   seq[6]: [seq[13], seq[14]],
                   seq[7]: [seq[15], seq[16]],
                   seq[8]: [seq[16], seq[17]]
                   }
        for indx in range(9, 18):
            tableau[seq[indx]] = {seq[indx + 9], seq[indx + 10]}
        for indx in range(18, 28):
            tableau[seq[indx]] = tuple()
        return tableau

    def drop_card(self, card):
        for parent, children in self.tableau.items():
            if card in children:
                children.remove(card)
        del self.tableau[card]


class Game:
    def __init__(self, seq, pile):
        self.count = 0
        self.tableau = Tableau(seq)
        self.pile = deque([Card(card) for card in pile])
        self.branches = deque([Branch(list())])
        self.paths = list()

    @which_watch
    def play(self):
        while self.branches:
            # print('count:', self.count, len(self.branches))
            self.count += 1
            branch = self.branches.popleft()
            tableau, pile, waste, path = branch.follow_path(self.tableau, self.pile)
            print("({}) {} branches, {}-long tableau, playing path {}".format(self.count,
                                                                              len(self.branches),
                                                                              len(tableau),
                                                                              path))
            if not tableau:
                print('Won!')
                return
            try:
                top_card = waste[0]
            except IndexError:
                top_card = pile.popleft()
                waste.appendleft(top_card)
            for parent, children in tableau.items():
                if not children and top_card.match(parent):
                    self.branches.append(Branch(path[:] + [parent]))
            if pile:
                self.branches.append(Branch(path[:] + ['f']))
            # print('BRANCHES:', self.branches)
        print('Lost!')


class Branch:
    def __init__(self, path):
        self.path = path
        # print('pathiepath', path)

    def __repr__(self):
        string = str()
        for card in self.path:
            if isinstance(card, Card):
                string += card.readable + " ~ "
            else:
                string += "flip ~ "
        try:
            return string[: -3]
        except IndexError:
            return string

    def follow_path(self, tableau, pile):
        # print("Following path:", self.path)
        tableau = deepcopy(tableau)
        pile = copy(pile)
        waste = deque()
        for step in self.path:
            # print(step, '~', pile)
            if isinstance(step, Card):
                self.move(tableau, pile, waste, step)
            else:
                self.move(tableau, pile, waste, None)
        return tableau, pile, waste, self.path

    @staticmethod
    def move(tableau, pile, waste, card):
        if card:
            tableau.drop_card(card)
            waste.appendleft(card)
        else:
            top_card = pile.popleft()
            waste.appendleft(top_card)


if __name__ == '__main__':
    example_seq = ['3h', '3d', '4d',
                   '6c', 'Ks', '8h', 'Ah', '8d', '7c',
                   'Qh', '10c', '7d', '5d', 'Jh', '9s', '4s', 'Kh', '3s',
                   '10s', '2d', 'Qs', '6h', 'Jd', '9h', 'As', '4c', '7h', '8s']
    example_pile = ['Kd', '2c', 'Ac', 'Qc', 'Js', '6s', '9d', '6d', 'Ac', '8c', '10d', '9c', '5c', '4h', '5s', '2s',
                    'Qd', '10h', 'Kc', 'Ad', '3c', '2h', '5h', '7s']
    # t = Tableau(example_seq)
    game = Game(example_seq, example_pile)
    game.play()
