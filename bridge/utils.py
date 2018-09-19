from collections import namedtuple
from random import shuffle
from copy import deepcopy

NS_PLAYERS = set(['N', 'S'])
EW_PLAYERS = set(['E', 'W'])


class Card(namedtuple('Card', ['suit', 'rank'])):
    __slots__ = ()
    rank_dict = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}
    suit_dict = {"S": 3, "H": 2, "D": 1, "C": 0}
    rank_string = '0123456789TJQKA'
    suit_string = 'CDHS'

    @classmethod
    def make_card(cls, card_string):
        suit = cls.suit_dict[card_string[0]]
        rank = cls.rank_dict[card_string[1]]
        return Card(suit=suit, rank=rank)

    def __repr__(self):
        return f'{self.suit_string[self.suit]}{self.rank_string[self.rank]}'


class BridgeGameState(object):
    next_player = {
        'N': 'E',
        'E': 'S',
        'S': 'W',
        'W': 'N'
    }

    def __init__(self):
        # Used by MCTS
        self.playerToMove = 'S'

        # Internal state
        self.player_hand = {
            'N': set(),
            'E': set(),
            'S': set(),
            'W': set()
        }
        self.trump = -1
        self.tricks = list()
        self.unseen_cards = set()
        self.ns_score = 0
        self.ew_score = 0

    def _init_deck(self, north_hand, south_hand, unseen_cards=None):
        assert len(north_hand) == len(south_hand)
        if unseen_cards is not None:
            assert len(north_hand) == len(unseen_cards) // 2

        self.unseen_cards.clear()
        self.player_hand['N'] = set(north_hand)
        self.player_hand['S'] = set(south_hand)
        self.remain_round = 0

        if unseen_cards is not None:
            self.unseen_cards = set(unseen_cards)
        else:
            for suit in range(4):
                for rank in range(2, 15):
                    card = Card(suit=suit, rank=rank)
                    if card not in north_hand and card not in south_hand:
                        self.cards_unseen.add(card)
        self.remain_round = len(north_hand)

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        state = deepcopy(self)
        return state

    def CloneAndRandomize(self, observer):
        """ Create a deep clone of this game state, randomizing any information not visible to the specified observer player.
        """
        state = self.Clone()
        cards = list(state.unseen_cards)
        shuffle(cards)

        trick_played = set(player for player, _ in state.tricks)
        hand_count = [state.remain_round - len(state.player_hand[player]) - (player in trick_played) for player in EW_PLAYERS]

        pre_count = 0
        for player, count in zip(EW_PLAYERS, hand_count):
            state.player_hand[player].update(cards[pre_count:pre_count + count])
            pre_count += count

        return state

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        card, current_player = move, self.playerToMove
        self.tricks.append((current_player, card))
        self.player_hand[current_player].discard(card)
        self.unseen_cards.discard(card)

        # Find out void
        if self.tricks[0][1].suit != card.suit and current_player in EW_PLAYERS:
            target_player = 'E' if current_player != 'E' else 'W'
            for c in list(self.unseen_cards):
                if c.suit == self.trick[0].suit:
                    self.unseen_cards.discard(c)
                    self.player_hand[target_player].add(c)

        # Deal with trick full
        if len(self.tricks) != 4:
            self.playerToMove = self.next_player[current_player]
        else:
            winner, winner_card = self.tricks[0]
            for trick_player, trick_card in self.tricks[1:]:
                if (trick_card.suit == winner_card.suit and trick_card.rank > winner_card.rank) or (trick_card.suit == self.trump and winner_card.suit != self.trump):
                    winner = trick_player
                    winner_card = trick_card
            if winner in NS_PLAYERS:
                self.ns_score += 1
            else:
                self.ew_score += 1
            self.playerToMove = winner
            self.tricks.clear()
            self.remain_round -= 1

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        hand = self.player_hand[self.playerToMove]

        moves = []
        if len(self.tricks) > 0:
            moves = [
                card
                for card in hand
                if card.suit == self.tricks[0][1].suit
            ]

        if not moves:
            moves = list(hand)

        return moves

    def GetResult(self, player):
        """ Get the game result from the viewpoint of player.
        """
        if player in NS_PLAYERS:
            return self.ns_score
        return self.ew_score

    def __repr__(self):
        """ Don't need this - but good style.
        """
        return f'{self.playerToMove}: ? Cards: {self.player_hand} Unseen: {self.unseen_cards}'
