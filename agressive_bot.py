import random
from typing import Optional
from schnapsen.game import Bot, PlayerPerspective, Move, SchnapsenTrickScorer, RegularMove
from schnapsen.deck import Card, Suit, Rank


class AggressiveBot(Bot):
    '''
    Aggressive bot that always plays the highest card. If there is a trump card available, it plays the highest rank trump card
    '''
    
    def __init__(self, rand: random.Random, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.rand = rand
            
            
    def get_move(self, player_perspective: PlayerPerspective, leader_move: Optional[Move], ) -> Move:
        
        valid_moves = player_perspective.valid_moves()

        moves_points: dict[Move, int] = {}
        
        if self.trump_available(player_perspective, leader_move):
                
            trump_suit: Suit = player_perspective.get_trump_suit()
            # Fill moves_points with all available trump cards in player deck
            for move in valid_moves:
                cards: list[Card] = move.cards
                current_card: Card = cards[0]
                card_rank: Rank = current_card.rank
                card_point: int = SchnapsenTrickScorer.SCORES.get(card_rank, 0)
                
                if current_card.suit == trump_suit:
                    moves_points[move] = card_point
                    

        else:
            # Fill moves_points with all available non-trump cards
            for move in valid_moves:
                cards: list[Card] = move.cards
                current_card: Card = cards[0]
                card_rank: Rank = current_card.rank
                card_point: int = SchnapsenTrickScorer.SCORES.get(card_rank, 0)

                moves_points[move] = card_point

        # Choose highest rank card from moves_points
        highest_rank: Move = max(moves_points, key = lambda k: moves_points[k])
        return highest_rank
            

    # First check if any trump cards are available
    def trump_available(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:     
        moves = perspective.valid_moves()
        for move in moves:
            if move.is_trump_exchange():
                return True
        return False
