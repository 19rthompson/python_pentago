BLACK = 1
WHITE = -1
BLANK = 0

class Board:

    def __init__(self):
        self.mSpaces = [BLANK]*36

    def getBoard(self):
        return self.mSpaces
    
    def placeMarble(self, position, color):
        if(position>=0 and position<=35 and color == BLACK or color == WHITE):
            if self.mSpaces[position]==BLANK:
                self.mSpaces[position]=color
                return True
        return False
    
    def rotateQuadrantRight(self, quadrant):
        if quadrant==1:
            start = 3
        elif quadrant==2:
            start = 0
        elif quadrant == 3:
            start = 18
        elif quadrant == 4:
            start = 21
        else:
            return False
        temp = self.mSpaces[start]
        self.mSpaces[start]=self.mSpaces[start+12]
        self.mSpaces[start+12]=self.mSpaces[start+14]
        self.mSpaces[start+14]=self.mSpaces[start+2]
        self.mSpaces[start+2]=temp
        temp=self.mSpaces[start+1]
        self.mSpaces[start+1]=self.mSpaces[start+6]
        self.mSpaces[start+6]=self.mSpaces[start+13]
        self.mSpaces[start+13]=self.mSpaces[start+8]
        self.mSpaces[start+8]=temp
        return True

    def rotateQuadrantLeft(self, quadrant):
        if quadrant==1:
            start = 3
        elif quadrant==2:
            start = 0
        elif quadrant == 3:
            start = 18
        elif quadrant == 4:
            start = 21
        else:
            return False
        temp = self.mSpaces[start]
        self.mSpaces[start]=self.mSpaces[start+2]
        self.mSpaces[start+2]=self.mSpaces[start+14]
        self.mSpaces[start+14]=self.mSpaces[start+12]
        self.mSpaces[start+12]=temp
        temp=self.mSpaces[start+1]
        self.mSpaces[start+1]=self.mSpaces[start+8]
        self.mSpaces[start+8]=self.mSpaces[start+13]
        self.mSpaces[start+13]=self.mSpaces[start+6]
        self.mSpaces[start+6]=temp
        return True

    def checkVictory(self):
        for i in range(12):
            if self.checkVictoryColumn(i) != BLANK:
                return self.checkVictoryColumn(i)
        
        for i in [0,1,6,7,12,13,18,19,24,25,30,31]:
            if self.checkVictoryRow(i):
                return self.checkVictoryRow(i)

        for i in [0,1,6,7]:
            if self.checkVictoryDiagonalRight(i):
                return self.checkVictoryDiagonalRight(i)
        
        for i in [4,5,10,11]:
            if self.checkVictoryDiagonalLeft(i):
                return self.checkVictoryDiagonalLeft(i)
        
        return False

    def checkVictoryColumn(self,start):
        if self.mSpaces[start]==self.mSpaces[start+6]==self.mSpaces[start+12]==self.mSpaces[start+18]==self.mSpaces[start+24]:
            return self.mSpaces[start]
        return BLANK

    def checkVictoryRow(self,start):
        if self.mSpaces[start]==self.mSpaces[start+1]==self.mSpaces[start+2]==self.mSpaces[start+3]==self.mSpaces[start+4]:
            return self.mSpaces[start]
        return BLANK

    def checkVictoryDiagonalRight(self,start):
        if self.mSpaces[start]==self.mSpaces[start+7]==self.mSpaces[start+14]==self.mSpaces[start+21]==self.mSpaces[start+28]:
            return self.mSpaces[start]
        return BLANK

    def checkVictoryDiagonalLeft(self,start):
        if self.mSpaces[start]==self.mSpaces[start+5]==self.mSpaces[start+10]==self.mSpaces[start+15]==self.mSpaces[start+20]:
            return self.mSpaces[start]
        return BLANK

    def printBoard(self):
        for i in range(36):
            if self.mSpaces[i]==BLANK:
                c='.'
            elif self.mSpaces[i]==WHITE:
                c='W'
            elif self.mSpaces[i]==BLACK:
                c='B'
            else:
                print("unexpected character in board")
                return False
            print(c,'', end="")
            if i%6==5:
                print()