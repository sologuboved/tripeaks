class TriPeaks:
    def __init__(self):
        self.pathways = self.generate_pathways()
        self.board = dict()
        self.deck = list()
        self.open = list(range(18, 28))

    def generate_pathways(self):
        pathways = {0: [3, 4], 1: [5, 6], 2: [7, 8]}
        start = 9
        second_row = dict()
        for card in pathways.values():
            second_row.update({card[0]: [start, start + 1], card[1]: [start + 1, start + 2]})
            start += 3
        pathways.update(second_row)
        for item in range(9, 18):
            pathways[item] = [start, start + 1]
            start += 1
        for card in self.open:
            pathways[card] = list()
        return pathways

    def fill_in_board(self, cards):
        for pos in range(len(cards)):
            self.board[pos] = cards[pos]

    def fill_in_deck(self, cards):
        self.deck.extend(cards)

    def play(self):
        pass

    def find_options(self):
        pass



class Game:
    def __init__(self, pathways, board, deck, open_pos, waste_card):
        self.pathways = pathways.copy()
        self.board = board.copy()
        self.deck = deck[:]
        self.open = open_pos[:]
        self.waste_card = waste_card

    def make_move(self):
        for pos in self.open:
            card = self.board[pos]
            if self.waste_card == card + 1 or self.waste_card == card - 1:
                pass




if __name__ == '__main__':
    t_p = TriPeaks()
    print(t_p.pathways)

