from bridge.utils import BridgeGameState, Card
from bridge.ismcts import ISMCTS

state = BridgeGameState()


north, south, unseen_cards = \
    [Card.make_card('CA'), Card.make_card('CQ')], \
    [Card.make_card('C3'), Card.make_card('C2')], \
    [Card.make_card('CK'), Card.make_card('C6'), Card.make_card('C5'), Card.make_card('C4')]

state._init_deck(north_hand=north, south_hand=south, unseen_cards=unseen_cards)
while True:
    print(state)
    if state.playerToMove in ['N', 'S']:
        find_card = ISMCTS(state, 1000, False)
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
