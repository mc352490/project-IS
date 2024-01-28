import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove
from schnapsen.deck import Card, Suit, Rank

class PassiveBot(Bot):
    # this initializes the passive bot with a random number generator and it has an optional name
    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.rand = rand
            
            
    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        # this gets a list of valid moves for the perspective of the current player
        valid_moves = player_perspective.valid_moves()

        # this creates a dictionary and stores the points that are associated with each of the moves
        moves_points: dict[Move, int] = {}

        if self.trump_available(player_perspective, leader_move):
            # it plays the lowest trump card if it is available and possible
            trump_moves = [move for move in valid_moves if move.is_trump_exchange()]
            return min(trump_moves, key=lambda move: move.cards[0].rank.value)

        else:
            # it plays the lowest non-trump card if there is no trump available
            non_trump_moves = [move for move in valid_moves if not move.is_trump_exchange()]
            return min(non_trump_moves, key=lambda move: move.cards[0].rank.value)

    def trump_available(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:     
        # it checks if trump cards are available in the current perspective of the player
        moves = perspective.valid_moves()
        for move in moves:
            if move.is_trump_exchange():
                return True
        return False
