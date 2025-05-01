BLANK = 0
BLACK = 1
WHITE = 2

I = 0
II = 1
III = 2
IV = 3

CCWISE = 0
CWISE = 1

import numpy as np


class Model: #pentago model

    def __init__(self):
        self.mSpaces = np.zeros((6,6),dtype = int)

    def getBoard(self):
        return self.mSpaces
    
    def reset(self):
        self.mSpaces = np.zeros((6,6),dtype = int)
    
    def placeMarble(self, row, column, color):
        if self.mSpaces[row][column]==BLANK:
            self.mSpaces[row][column]=color
    
    def rotateQuadrantLeft(self, quadrant):
        if quadrant==I:
            start = (0,3)
        elif quadrant==II:
            start = (0,0)
        elif quadrant == III:
            start = (3,0)
        elif quadrant == IV:
            start = (3,3)
        else:
            return False
        temp = self.mSpaces[start]
        self.mSpaces[start[0]][start[1]]=self.mSpaces[start[0]][start[1]+2]
        self.mSpaces[start[0]][start[1]+2]=self.mSpaces[start[0]+2][start[1]+2]
        self.mSpaces[start[0]+2][start[1]+2]=self.mSpaces[start[0]+2][start[1]]
        self.mSpaces[start[0]+2][start[1]]=temp

        temp=self.mSpaces[start[0]][start[1]+1]
        self.mSpaces[start[0]][start[1]+1]=self.mSpaces[start[0]+1][start[1]+2]
        self.mSpaces[start[0]+1][start[1]+2]=self.mSpaces[start[0]+2][start[1]+1]
        self.mSpaces[start[0]+2][start[1]+1]=self.mSpaces[start[0]+1][start[1]]
        self.mSpaces[start[0]+1][start[1]]=temp
        return True
    
    def rotateQuadrantLeftState(self, state, quadrant):
        if quadrant==I:
            start = (0,3)
        elif quadrant==II:
            start = (0,0)
        elif quadrant == III:
            start = (3,0)
        elif quadrant == IV:
            start = (3,3)
        else:
            return False
        temp = state[start]
        state[start[0]][start[1]]=state[start[0]][start[1]+2]
        state[start[0]][start[1]+2]=state[start[0]+2][start[1]+2]
        state[start[0]+2][start[1]+2]=state[start[0]+2][start[1]]
        state[start[0]+2][start[1]]=temp

        temp=state[start[0]][start[1]+1]
        state[start[0]][start[1]+1]=state[start[0]+1][start[1]+2]
        state[start[0]+1][start[1]+2]=state[start[0]+2][start[1]+1]
        state[start[0]+2][start[1]+1]=state[start[0]+1][start[1]]
        state[start[0]+1][start[1]]=temp
        return state

    def rotateQuadrantRight(self, quadrant):
        if quadrant==I:
            start = (0,3)
        elif quadrant==II:
            start = (0,0)
        elif quadrant == III:
            start = (3,0)
        elif quadrant == IV:
            start = (3,3)
        else:
            return False
        
        temp = self.mSpaces[start]
        self.mSpaces[start[0]][start[1]] = self.mSpaces[start[0]+2][start[1]]
        self.mSpaces[start[0]+2][start[1]] = self.mSpaces[start[0]+2][start[1]+2]
        self.mSpaces[start[0]+2][start[1]+2] = self.mSpaces[start[0]][start[1]+2]
        self.mSpaces[start[0]][start[1]+2] = temp

        temp = self.mSpaces[start[0]+1][start[1]]
        self.mSpaces[start[0]+1][start[1]] = self.mSpaces[start[0]+2][start[1]+1]
        self.mSpaces[start[0]+2][start[1]+1] = self.mSpaces[start[0]+1][start[1]+2]
        self.mSpaces[start[0]+1][start[1]+2] = self.mSpaces[start[0]][start[1]+1]
        self.mSpaces[start[0]][start[1]+1] = temp
        return True
    
    def rotateQuadrantRightState(self, state, quadrant):
        if quadrant==I:
            start = (0,3)
        elif quadrant==II:
            start = (0,0)
        elif quadrant == III:
            start = (3,0)
        elif quadrant == IV:
            start = (3,3)
        else:
            return False
        
        temp = state[start]
        state[start[0]][start[1]] = state[start[0]+2][start[1]]
        state[start[0]+2][start[1]] = state[start[0]+2][start[1]+2]
        state[start[0]+2][start[1]+2] = state[start[0]][start[1]+2]
        state[start[0]][start[1]+2] = temp

        temp = state[start[0]+1][start[1]]
        state[start[0]+1][start[1]] = state[start[0]+2][start[1]+1]
        state[start[0]+2][start[1]+1] = state[start[0]+1][start[1]+2]
        state[start[0]+1][start[1]+2] = state[start[0]][start[1]+1]
        state[start[0]][start[1]+1] = temp
        return state
    
    

    def checkVictory(self):
        for r in range(6):
            row_array = [int(i) for i in list(self.mSpaces[r, :])]
            for c in range(2):
                # Create a horizontal window of 5
                window = row_array[c:c + 5]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]
        
        # Score vertical positions
        for c in range(6):
            col_array = [int(i) for i in list(self.mSpaces[:, c])]
            for r in range(2):
                # Create a vertical window of 5
                window = col_array[r:r + 5]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]

        # Score Negative diagonals
        
        for r in range(2):
            for c in range(2):
                # Create a positive diagonal window of 4
                window = [self.mSpaces[r + i][c + i] for i in range(5)]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]
            
        # Score Positive diagonals
        for r in [5,4]:
            for c in range(2):
                window = [self.mSpaces[r - i][c + i] for i in range(5)]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]
        return BLANK
    
    def checkVictoryState(self, state):
        for r in range(6):
            row_array = [int(i) for i in list(state[r, :])]
            for c in range(2):
                # Create a horizontal window of 5
                window = row_array[c:c + 5]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]
        
        # Score vertical positions
        for c in range(6):
            col_array = [int(i) for i in list(state[:, c])]
            for r in range(2):
                # Create a vertical window of 5
                window = col_array[r:r + 5]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]

        # Score Negative diagonals
        
        for r in range(2):
            for c in range(2):
                # Create a positive diagonal window of 4
                window = [state[r + i][c + i] for i in range(5)]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]
            
        # Score Positive diagonals
        for r in [5,4]:
            for c in range(2):
                window = [state[r - i][c + i] for i in range(5)]
                if window[0] == window[1] == window[2] == window[3] == window [4] and window[0]:
                    return window[0]
        return BLANK

    

    def printBoard(self):
        for i in range(6):
            for j in range(6):
                if self.mSpaces[i][j]==BLANK:
                    c='.'
                elif self.mSpaces[i][j]==WHITE:
                    c='W'
                elif self.mSpaces[i][j]==BLACK:
                    c='B'
                else:
                    print("unexpected character in board")
                    return False
                print(c,'', end="")
            print()

    def rotate(self,quadrant,direction):
        if direction == CWISE:
            self.rotateQuadrantRight(quadrant)
        elif direction == CCWISE:
            self.rotateQuadrantLeft(quadrant)

    def rotateState(self, state, quadrant, direction):
        if direction == CWISE:
            return self.rotateQuadrantRightState(state, quadrant)
        else:
            return self.rotateQuadrantLeftState(state, quadrant)

    def ACTIONS(self,state):
        actions = []
        for r in range(6):
            for c in range(6):
                if state[r][c]!=BLANK:
                    continue
                for q in range(4):
                    for d in range(2):
                        actions.append([r,c,q,d])
        return actions

    def move(self,action,color):
        self.placeMarble(action[0],action[0],color)
        self.rotate(action[2],action[3])
        return self.mSpaces
    
    def moveState(self, state, action, color):
        state[action[0]][action[1]] = color
        state = self.rotateState(state, action[2], action[3])
        return state


        

def main():
    board = Model()
    """board.placeMarble(0,0,BLACK)
    board.placeMarble(5,0,WHITE)

    board.rotateQuadrantRight(II)
    board.printBoard(); print()

    board.rotateQuadrantRight(II)
    board.printBoard(); print()

    board.rotateQuadrantRight(II)
    board.printBoard(); print()

    board.rotateQuadrantRight(II)
    board.printBoard()"""
    board.mSpaces = np.array([[BLACK,BLANK,BLANK,BLANK,BLANK,WHITE],
                              [BLANK,BLACK,BLANK,BLANK,WHITE,BLANK],
                              [BLANK,BLANK,BLANK,WHITE,BLANK,BLANK],
                              [BLANK,BLANK,WHITE,BLACK,BLANK,BLANK],
                              [BLANK,WHITE,BLANK,BLANK,BLACK,BLANK],
                              [WHITE,BLANK,BLANK,BLANK,BLANK,BLANK]])
    board.printBoard()
    print(board.checkVictory())




    

if __name__ == "__main__":
    main()