#!/usr/bin/env python3

# import rock_paper_scissors.rock_paper_scissorsv0 as rps
import pentago_game.pentago_game as pen
from pentago_game.env.PentagoModel import Model
import random, time
import numpy as np
import copy

BLANK = 0
BLACK = 1
WHITE = 2

RIGHT=0
LEFT=1

I = 0
II = 1
III = 2
IV = 3

CCWISE = 0
CWISE = 1



def main():
    numGames = 1
    numMovesTotal = 0
    numWonGames = 0
    numLostGames = 0
    numTiedGames = 0
    


    global CUTOFF_DEPTH
    for i in range(numGames):
        env = pen.env(render_mode="ansi")
        env.reset()
        flag=0
        numMovesLocal = 0
        
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            
            if termination or truncation:
                action = None
            else:
                
                if flag == 0 and not (termination or truncation):
                    CUTOFF_DEPTH = 2              
                    #action = random_agent(env,observation,agent)                
                    #action = human_agent(observation,agent)
                    action = minimax_agent(observation, agent)
                    
                    
                    flag+=1
                elif flag == 1 and not (termination or truncation):
                    CUTOFF_DEPTH = 2
                    #action = random_agent(env,observation,agent)
                    #action = human_agent(observation,agent)
                    action = minimax_agent(observation, agent)
                    
                    flag -=1

                
                    
            env.step(action)
            numMovesLocal+=1
        
        if reward == 1:
            numMovesTotal += numMovesLocal
            numWonGames += 1
        if reward == -1:
            numLostGames += 1
        else:
            numTiedGames +=1

        env.close()
    print("Average Number of moves to win:",numMovesTotal / numWonGames)
    print("Percent of Games Won", numWonGames/500)

def random_agent(env,observation,agent):
    while True:
        action = env.action_space(agent).sample()
        if observation[action[0]][action[1]] == BLANK:
            return action
        
def human_agent(observation,agent):
    humanModel = Model()
    humanModel.mSpaces = observation.copy()
    
    while True:
        action = [int(input("Enter row (0-5):")),int(input("Enter column (0-5):")),int(input("Enter quadrant (0-3):")),int(input("Enter Direction (0-1):"))]
        if observation[action[0]][action[1]] == BLANK:
            return action
        else: 
            print("Invalid action")
    


ROW_COUNT = 6
COLUMN_COUNT = 6
WINDOW_LENGTH = 5
def evaluate(board,agent):
    if agent == "player_0":
        color = 1
    elif agent == "player_1":
        color = 2
    elif agent == 1:
        color = 1
    elif agent == 2:
        color = 2

    score = 0
    # add center spaces
    
    
    for r in [1,4]:
        for c in [1,4]:
            if board[r][c] == color:
                score += 10
        for c in [2,3]:
            if board[r][c] == color:
                score += 2
    for r in [3,4]:
        for c in [1,4]:
            if board[r][c] == color:
                score+=2

                
                
    
    # Score horizontal positions
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        
        for c in range(2):
            # Create a horizontal window of 5
            window = row_array[c:c + WINDOW_LENGTH]
            
            score += evaluate_window(window, color)
        #time.sleep(.4)

    # Score vertical positions
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(2):
            # Create a vertical window of 5
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, color)

    # Score positive diagonals
    for r in range(2):
        for c in range(2):
            # Create a positive diagonal window of 4
            window = [board[r + i][c + i] for i in range(5)]
            score += evaluate_window(window, color)

    """# Score negative diagonals
    for r in range(ROW_COUNT - 4):
        for c in range(COLUMN_COUNT - 4):
            # Create a negative diagonal window of 4
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)"""
    """print("Color =",color)
    print("Score =",score)
    print("Board:\n",board); print()"""
    return score

def evaluate_window(window, piece):
    score = 0
    # Switch scoring based on turn
    opp_piece = BLACK
    if piece == BLACK:
        opp_piece = WHITE

    # Prioritise a winning move
    # Minimax makes this less important
    if window.count(piece) == 5:
        score += 1000000000
    # Make connecting 3 second priority
    elif window.count(piece) == 4:
        score += 200
    elif window.count(piece) == 3 and window.count(BLANK) >=1:
        score += 80
    # Make connecting 2 third priority
    elif window.count(piece) >= 2 and window.count(BLANK) >= 2:
        score += 10
    # Prioritise blocking an opponent's winning move (but not over winning)
    # Minimax makes this less important
    if window.count(opp_piece) == 4 and window.count(BLANK) == 1:
        score -= 900
    elif window.count(opp_piece) == 3 and window.count(BLANK) == 2:
        score-=500

    return score



# pseudo code

def minimax_agent(initial_state, agent):
    depth = 0
    if agent == "player_0":
        color = BLACK
    elif agent == "player_1":
        color = WHITE
    best_value = -1000
    best_action = None
    for action in Model().ACTIONS(initial_state):
        next_state = Model().moveState(copy.deepcopy(initial_state),action,color)
        value = MIN(next_state, color, depth+1)
        if value > best_value:
            best_value = value
            best_action = action
    return best_action
    

def MAX(current_state, color, depth):
    if depth >= CUTOFF_DEPTH or Model().checkVictoryState(current_state):
        return evaluate(current_state,color)
    best_value = -10000
    for action in Model().ACTIONS(current_state):
        next_state = Model().moveState(current_state, action, color)
        value = MIN(copy.deepcopy(next_state), color, depth+1)
        if value > best_value:
            best_value = value
    return best_value

def MIN(current_state, color, depth):
    if depth >= CUTOFF_DEPTH or Model().checkVictoryState(current_state):
        return evaluate(current_state, color)
    best_value = 10000
    for action in Model().ACTIONS(current_state):
        next_state = Model().moveState(copy.deepcopy(current_state),action, color)
        value = MAX(next_state, color, depth+1)
        if value < best_value:
            best_value = value
    return best_value


    




if __name__ == "__main__":
    main()