from copy import copy, deepcopy
from collections import deque
from basic_operations import which_watch


class Card:
    def __init__(self, raw_card):
        self.mapper = {'J': 11, 'Q': 12, 'K': 13, 'A': 1}
        self.inv_mapper = {val: key for key, val in self.mapper.items()}
        self.readable = raw_card
        self.card = self.process_card()

    def __eq__(self, other):
        return self.readable == other.readable

    def __repr__(self):
        return "'{}'".format(self.readable)

    def __hash__(self):
        return hash(repr(self))

    def process_card(self):
        rank = self.readable[: -1]
        return int(self.mapper.get(rank, rank)), self.readable[-1]

    def match(self, other):
        rank, other_rank = [card[0] for card in (self.card, other.card)]
        return abs(rank - other_rank) in (1, 12)


class Tableau:
    def __init__(self, seq):
        self.tableau = self.fill_in(seq)

    def __getitem__(self, item):
        return self.tableau[item]

    def __iter__(self):
        for parent in self.tableau:
            yield parent

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
                   seq[8]: [seq[16], seq[17]]}
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
        self.pile = [Card(card) for card in pile]
        self.branches = deque([Branch(list())])
        self.paths = list()

    # @which_watch
    def play(self, printer_on=False):
        while self.branches:
            self.count += 1
            branch = self.branches.popleft()
            tableau, pile, top_card, path = branch.follow_path(self.tableau, self.pile)
            if printer_on:
                print("({}) {} branches, {} cards, path {}".format(self.count, len(self.branches), len(tableau), path))
            else:
                print("\r   {}".format(self.count), end=str(), flush=True)
            if not tableau:
                print('\nWon!')
                return True
            dropped = False
            for parent, children in tableau.items():
                if not children and top_card.match(parent):
                    self.branches.appendleft(Branch(path[:] + [parent]))
                    dropped = True
            if pile:
                if dropped:
                    self.branches.append(Branch(path[:] + ['f ' + pile[0].readable]))
                else:
                    self.branches.appendleft(Branch(path[:] + ['f ' + pile[0].readable]))
        print('\nLost!')
        return False


class Branch:
    def __init__(self, path):
        self.path = path

    def follow_path(self, tableau, pile):
        tableau = deepcopy(tableau)
        pile = copy(pile)
        top_card = pile.pop(0)
        for step in self.path:
            if isinstance(step, Card):
                tableau.drop_card(step)
                top_card = step
            else:
                top_card = pile.pop(0)
        return tableau, pile, top_card, self.path


if __name__ == '__main__':
    # example_seq = ['3h', '3d', '4d',
    #                '6c', 'Ks', '8h', 'Ah', '8d', '7c',
    #                'Qh', '10c', '7d', '5d', 'Jh', '9s', '4s', 'Kh', '3s',
    #                '10s', '2d', 'Qs', '6h', 'Jd', '9h', 'As', '4c', '7h', '8s']
    # example_pile = ['Kd', '2c', 'Ac', 'Qc', 'Js', '6s', '9d', '6d', 'Jc', '8c', '10d', '9c', '5c', '4h', '5s', '2s',
    #                 'Qd', '10h', 'Kc', 'Ad', '3c', '2h', '5h', '7s']
    # example_seq = ['2c', '9h', 'Jh',
    #                '6d', 'Jd', '10c', 'Qh', '3c', 'Qs',
    #                '2s', 'Kh', 'Ah', '5h', '4s', '7h', 'Kd', '9c', '10s',
    #                'Ks', '4d', '5s', '5c', '6c', '6s', '3d', '3s', '8c', 'Js']
    # example_pile = ['Qc', '2h', '8h', 'Ad', 'Ac', 'Qd', '3h', 'Kc', '8d', '8s', '9s', '4h', '9d', '7s', '5d', 'As',
    #                 '10d', '6h', '10h', '7c', '7d', '2d', '4c', 'Jc']
    example_seq = ['10s', '6d', 'As',
                   'Qs', 'Ah', '8c', '8d', '4s', '2s',
                   '4h', '7h', '7d', '10d', 'Qd', 'Ac', 'Ad', 'Jd', '6s',
                   '3s', '9d', '2c', '9c', '3c', '5c', '2h', 'Kc', '7c', 'Jh']
    example_pile = ['4c', 'Js', 'Qc', '4d', '3d', '5h', '9s', '10c', '3h', '8h', '7s', '5s', '6c', 'Qh', 'Ks', '9h',
                    '2d', '10h', '8s', '5d', 'Kh', 'Kd', 'Jc', '6h']
    game = Game(example_seq, example_pile)
    game.play()
