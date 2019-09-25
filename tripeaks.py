from copy import deepcopy
from collections import deque


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

    def __str__(self):
        string = str()
        for parent in sorted(self.tableau.keys()):
            string += "{}: {}\n".format(parent.readable,
                                        ", ".join(sorted([child.readable for child in self.tableau[parent]])))
        return string

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
        self.tableau = Tableau(seq)
        self.pile = deque([Card(card) for card in pile])
        self.waste = deque([self.pile.pop(0)])
        self.branches = deque()

    def __repr__(self):
        return [card.readable for card in self.pile]

    def play(self):
        pass


class Branch:
    def __init__(self, tableau, pile, waste):
        self.tableau = deepcopy(tableau)
        self.pile = deepcopy(pile)
        self.waste = deepcopy(waste)


if __name__ == '__main__':
    example_seq = ['3h', '3d', '4d',
                   '6c', 'Ks', '8h', 'Ah', '8d', '7c',
                   'Qh', '10c', '7d', '5d', 'Jh', '9s', '4s', 'Kh', '3s',
                   '10s', '2d', 'Qs', '6h', 'Jd', '9h', 'As', '4c', '7h', '8s']
    t = Tableau(example_seq)
    for c in t:
        print(c)
