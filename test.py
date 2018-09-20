from bridge.utils import BridgeGameState, Card
from bridge.ismcts import ISMCTS

state = BridgeGameState()

# 50%
# north, south, unseen_cards = \
#     [Card.make_card('CA'), Card.make_card('CQ')], \
#     [Card.make_card('C3'), Card.make_card('C2')], \
#     [Card.make_card('CK'), Card.make_card('C6'), Card.make_card('C5'), Card.make_card('C4')]

# 50%-50%
# north, south, unseen_cards = \
#     [Card.make_card('CA'), Card.make_card('CJ'), Card.make_card('CT')], \
#     [Card.make_card('CK'), Card.make_card('C9'), Card.make_card('C8')], \
#     [Card.make_card('CQ'), Card.make_card('C6'), Card.make_card('C5'), Card.make_card('C4'), Card.make_card('C3'), Card.make_card('C2')]

# 8-Finesse
# north, south, unseen_cards = \
#     [Card.make_card('CA'), Card.make_card('CJ'), Card.make_card('CT'), Card.make_card('C9')], \
#     [Card.make_card('CK'), Card.make_card('C8'), Card.make_card('C7'), Card.make_card('C6')], \
#     [Card.make_card('CQ'), Card.make_card('C5'), Card.make_card('C4'), Card.make_card('C3'), Card.make_card('C2'),
#         Card.make_card('H4'), Card.make_card('H3'), Card.make_card('H2')]


# 9-Knockout
north, south, unseen_cards = \
    [Card.make_card('CA'), Card.make_card('CJ'), Card.make_card('CT'), Card.make_card('C9'), Card.make_card('C8')], \
    [Card.make_card('CK'), Card.make_card('C7'), Card.make_card('C6'), Card.make_card('C5'), Card.make_card('H2')], \
    [Card.make_card('CQ'), Card.make_card('C4'), Card.make_card('C3'), Card.make_card('C2'),
        Card.make_card('H8'), Card.make_card('H7'), Card.make_card('H6'), Card.make_card('H5'), Card.make_card('H4'), Card.make_card('H3')]


state._init_deck(north_hand=north, south_hand=south, unseen_cards=unseen_cards, trump=0)

while True:
    print(state)
    if state.playerToMove in ['N', 'S']:
        find_card = ISMCTS(state, 1000, exploration=state.remain_round, verbose=False)
        candidate_cards = state.GetMoves()
    else:
        candidate_cards = list(state.unseen_cards | state.player_hand[state.playerToMove])
    card_str = input(f'Enter the card {candidate_cards}: ')
    try:
        card = Card.make_card(card_str)
        assert card in candidate_cards
    except Exception as e:
        print('Wrong card!')
        continue
    state.DoMove(card)
