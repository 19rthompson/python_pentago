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
    global CUTOFF_DEPTH
    env = pen.env(render_mode="ansi")
    env.reset()
    flag=0
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        
        if termination or truncation:
            action = None
        else:
            
            if flag == 0 and not (termination or truncation):
                CUTOFF_DEPTH = 1              
                #action = random_agent(env,observation,agent)
                #action = single_agent_1(observation,agent)
                #action = human_agent(observation,agent)
                action = minimax_agent(observation, agent)
                
                
                flag+=1
            elif flag == 1 and not (termination or truncation):
                CUTOFF_DEPTH = 1
                #action = random_agent(env,observation,agent)
                #action = single_agent_1(observation,agent)
                #action = human_agent(observation,agent)
                action = minimax_agent(observation, agent)
                
                flag -=1

            
                
        env.step(action)
    
        
    print(reward)    
    env.close()

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
    


def single_agent_1(observation,agent):
    if(agent == "player_0" ):
        color = BLACK
    elif (agent == "player_1"):
        color = WHITE
    model = Model()
    
    model.mSpaces = np.array(observation)
    max_score = -99999999999999
    max_move = None

    for action in model.ACTIONS():
        model.placeMarble(action[0],action[1],color)
        model.rotate(action[2],action[3])
        score = evaluate_2(model.getBoard(),agent)
        if score > max_score:
            max_score = score
            max_move = action
        model.mSpaces = np.array(observation)

    
    
    return max_move


ROW_COUNT = 6
COLUMN_COUNT = 6
WINDOW_LENGTH = 5
def evaluate_2(board,agent):
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
                score += 5
                
                
    
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

    """# Score positive diagonals
    for r in range(ROW_COUNT - 4):
        for c in range(COLUMN_COUNT - 4):
            # Create a positive diagonal window of 4
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, color)

    # Score negative diagonals
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
        score += 1000
    # Make connecting 3 second priority
    elif window.count(piece) == 4:
        score += 30
    # Make connecting 2 third priority
    elif window.count(piece) >= 2 and window.count(BLANK) <= 2:
        
        score += 1
    # Prioritise blocking an opponent's winning move (but not over winning)
    # Minimax makes this less important
    if window.count(opp_piece) == 4 and window.count(BLANK) == 1:
        score -= 20

    return score




def evaluate_1(modelBoard,agent):
    score = 0
    oppcolor = 1
    if agent == "player_0":
        color = 1
        oppcolor = 2
    elif agent == "player_1":
        color = 2
    for i in [7,10,25,28]:
        if modelBoard[i]==color:
            score += 5
    score += evaluate_windows_1(modelBoard,color,oppcolor)   

    

    return score

def evaluate_windows_1(modelBoard,color,oppcolor):
    score = 0
    hWindows = np.array([0,1,6,7,12,13,18,19,24,25,30,31],dtype=int)
    vWindows = range(12)
    dWindowsLeft = np.array([0,1,6,7],dtype = int)
    dWindowsRight = np.array([4,5,10,11],dtype = int)

    #score horizontal windows
    for space in hWindows:
        window = np.zeros(5,dtype = int)
        for i in range(5):
            window[i] = modelBoard[space+1]
        counts = np.bincount(window)
        if len(counts<3):
            counts = np.append(counts,0)
        if len(counts<3):
            counts = np.append(counts,0)
        if counts[color] == 5:
            score += 1000
        elif counts[color] == 4 and counts[BLANK] == 1:
            score += 10
        elif counts[color] == 3 and counts[BLANK] >= 1:
            score += 8
        elif counts[color] == 2 and counts[BLANK] >= 1:
            score += 2
        elif len(counts)>2 and counts[oppcolor] == 5:
            score -= 1000

    #score vertical windows
    for space in vWindows:
        window = np.zeros(5,dtype = int)
        for i in range(5):
            window[i] = modelBoard[space + (i * 6)]
        counts = np.bincount(window)
        if len(counts<3):
            counts = np.append(counts,0)
        if len(counts<3):
            counts = np.append(counts,0)
        if counts[color] == 5:
            score += 1000
        elif counts[color] == 4 and counts[BLANK] == 1:
            score += 10
            
        elif counts[color] == 3 and counts[BLANK] >= 1:
            score += 8
        elif counts[color] == 2 and counts[BLANK] >= 1:
            score += 2
        elif len(counts)>2 and counts[oppcolor] == 5:
            score -= 1000

    #score diagonal windows
    for space in dWindowsLeft:
        window = np.zeros(5,dtype = int)
        for i in range(5):
            window[i] = modelBoard[space + (i+7)]
        counts = np.bincount(window)
        if len(counts<3):
            counts = np.append(counts,0)
        if len(counts<3):
            counts = np.append(counts,0)
        if counts[color] == 5:
            score += 1000
        elif counts[color] == 4 and counts[BLANK] == 1:
            
            score += 10
        elif counts[color] == 3 and counts[BLANK] >= 1:
            score += 8
        elif counts[color] == 2 and counts[BLANK] >= 1:
            score += 2
        elif len(counts)>2 and counts[oppcolor] == 5:
            score -= 1000

    for space in dWindowsRight:
        window = np.zeros(5,dtype = int)
        for i in range(5):
            window[i] = modelBoard[space + (i+5)]
        counts = np.bincount(window)
        if len(counts<3):
            counts = np.append(counts,0)
        if len(counts<3):
            counts = np.append(counts,0)
        if counts[color] == 5:
            score += 1000
        elif counts[color] == 4 and counts[BLANK] == 1:
            score += 10
        elif counts[color] == 3 and counts[BLANK] >= 1:
            score += 8
        elif counts[color] == 2 and counts[BLANK] >= 1:
            score += 2
        elif len(counts)>2 and counts[oppcolor] == 5:
            score -= 1000

    return score



def minimax_agent(state, agent):
    oppcolor = 1
    if agent == "player_0":
        color = 1
        oppcolor = 2
    elif agent == "player_1":
        color = 2

    depth = 0    
    best_value = -2000
    best_action = None
    for action in Model().ACTIONS(state):
        next_state = copy.deepcopy(Model().moveState(copy.deepcopy(state), action, color))
        #print("next state before min:\n", next_state)
        value = MIN(next_state, depth+1, color)
        #print("next state after min:\n",next_state)
        next_state = copy.deepcopy(state)
        #print("next state after resetting:\n",next_state)
        #time.sleep(10)
        if value > best_value:
            best_value = value
            best_action = action
    return best_action
    

def MAX(current_state,depth,color):
    #print("maxState:\n",current_state)
    if depth >= CUTOFF_DEPTH or Model().checkVictoryState(current_state):
        return evaluate_2(current_state,color)
    best_value = -2000
    for action in Model().ACTIONS(current_state):
        next_state = copy.deepcopy(Model().moveState(copy.deepcopy(current_state), action, color))
        value = MIN(next_state, depth+1, color)
        next_state = copy.deepcopy(current_state)
        
        if value > best_value:
            best_value = value
    return best_value


def MIN(current_state,depth,color):
    
    
    if depth >= CUTOFF_DEPTH or Model().checkVictoryState(current_state):
        return evaluate_2(current_state,color)
    best_value = 100000
    
    for action in Model().ACTIONS(current_state):

        next_state = copy.deepcopy(Model().moveState(copy.deepcopy(current_state), action, color))
        
        value = MAX(next_state, depth+1, color)

        next_state = copy.deepcopy(current_state)
        
        
        if value < best_value:
            best_value = value
    return best_value






if __name__ == "__main__":
    main()