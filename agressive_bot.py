import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove
from schnapsen.deck import Card, Suit

class AgressiveBot(Bot):
    def _init_(self, rand: random.Random, name: Optional[str] = None) -> None:
        super()._init_(name)
        self.rand = rand

    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        
        # als bot is leader, dan leg altijd hoogste trump

        # als tegenstander is leader:
        # - legt non-trump card, dan leg random trump card, of leg card hoger dan tegenstander
        # - legt trump card, dan leg hogere trump, zo niet dan leg laagste card
        # 
        
        valid_moves = player_perspective.valid_moves()

        moves_points: dict[Move, int] = []

        if self.trump_available(player_perspective, leader_move):
                
            trump_suit: Suit = player_perspective.get_trump_suit()

            for move in valid_moves:
                cards: list[Card] = move.cards
                current_card: Card = cards[0]
                card_point: int = SchnapsenTrickScorer().rank_to_points(current_card)
                
                if current_card == trump_suit:
                    moves_points[move] = card_point

        else:
            
            for move in valid_moves:
                cards: list[Card] = move.cards
                current_card: Card = cards[0]
                card_point: int = int = SchnapsenTrickScorer().rank_to_points(current_card)

                moves_points[move] = card_point

        highest_rank: Move = max(moves_points, key = lambda k: moves_points[k])
        return highest_rank
            
    def trump_available(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:     
        moves = perspective.valid_moves()
        for move in moves:
            if move.is_trump_exchange():
                return True
        return False
    
