"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    best_move = (-1, -1)
    best_score = -2
    
    winner = board.check_win()
    if winner:
        # base case
        return (SCORES[board.check_win()], best_move)
    else:
        # recursive case
        poss_moves = board.get_empty_squares()
        next_player = provided.switch_player(player)
        for poss_move in poss_moves:
            board_clone = board.clone()
            board_clone.move(poss_move[0], poss_move[1], player)
            
            score, dummy_var = mm_move(board_clone, next_player)
            
            if score * SCORES[player] > best_score:
                best_score = score * SCORES[player]
                best_move = poss_move
            if best_score == 1:
                break
    
    return (best_score * SCORES[player], best_move)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


#gameboard = provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERO, provided.PLAYERX],
#                                         [provided.EMPTY, provided.PLAYERO, provided.EMPTY],
#                                         [provided.EMPTY, provided.EMPTY, provided.PLAYERO]])
#gameboard = provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX, provided.PLAYERX],
#                                         [provided.PLAYERO, provided.PLAYERX, provided.EMPTY],
#                                         [provided.EMPTY, provided.PLAYERO, provided.PLAYERX]])
#print gameboard
#print mm_move(gameboard, provided.PLAYERX)
