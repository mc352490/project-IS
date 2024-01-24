import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove
from schnapsen.deck import Card, Suit, Rank

class PassiveBot(Bot):
    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.rand = rand
            
            
    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        valid_moves = player_perspective.valid_moves()

        moves_points: dict[Move, int] = {}

        if self.trump_available(player_perspective, leader_move):
            # Zo speel je altijd de laagste trump card als die er is
            trump_moves = [move for move in valid_moves if move.is_trump_exchange()]
            return min(trump_moves, key=lambda move: move.cards[0].rank.value)

        else:
            # speel je de laagste non-trump card
            non_trump_moves = [move for move in valid_moves if not move.is_trump_exchange()]
            return min(non_trump_moves, key=lambda move: move.cards[0].rank.value)

    def trump_available(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:     
        moves = perspective.valid_moves()
        for move in moves:
            if move.is_trump_exchange():
                return True
        return False
