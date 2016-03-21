"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 500         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.

def mc_trial(board, player):
    """
    Plays out on given board with random moves until one player wins
    """
    while board.check_win() == None:
        emp_sqrs = board.get_empty_squares()
        chosen_sq = random.choice(emp_sqrs)
        board.move(chosen_sq[0], chosen_sq[1], player)
        player = provided.switch_player(player)
    return

def mc_update_scores(scores, board, mach_player):
    """
    Updates scores with a completed board
    """
    sqrs = [(row_num, col_num) for row_num in range(board.get_dim()) for col_num in range(board.get_dim())]
    if board.check_win() == mach_player:
        for sqr in sqrs:
            if board.square(sqr[0], sqr[1]) == mach_player:
                scores[sqr[0]][sqr[1]] += SCORE_CURRENT
            elif board.square(sqr[0], sqr[1]) == provided.switch_player(mach_player):
                scores[sqr[0]][sqr[1]] -= SCORE_OTHER
    elif board.check_win() == provided.switch_player(mach_player):
        for sqr in sqrs:
            if board.square(sqr[0], sqr[1]) == mach_player:
                scores[sqr[0]][sqr[1]] -= SCORE_CURRENT
            elif board.square(sqr[0], sqr[1]) == provided.switch_player(mach_player):
                scores[sqr[0]][sqr[1]] += SCORE_OTHER

def get_best_move(board, scores):
    """
    Selects best move from scores
    """
    all_scores = {}
    for row_num in range(board.get_dim()):
        for col_num in range(board.get_dim()):
            if board.square(row_num, col_num) == provided.EMPTY:
                all_scores [(row_num, col_num)] = scores[row_num][col_num]
    max_score = max(all_scores.values())
    max_sqrs = []
    for sqr in all_scores:
        if all_scores[sqr] == max_score:
            max_sqrs.append(sqr)
    return random.choice(max_sqrs)

def mc_move(board, player, trials):
    """
    Returns best move
    """
    scores = [[0 for dummy_x in range(board.get_dim())] for dummy_x in range(board.get_dim())]
    for dummy_num in range(trials):
        check_board = board.clone()
        mc_trial(check_board, player)
        mc_update_scores(scores, check_board, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, mc_move, NTRIALS, False)
