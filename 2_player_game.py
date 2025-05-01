from Board import *

board = Board()

print("Welcome to 2-Player Pentago")
board.printBoard()
while True:
    while True: #get input for marble placement for black
        move = input("Black, place your marble (integer): ")
        if int(move) in range(36) and board.placeMarble(int(move),BLACK):
            break
        print("Not a valid position. Try again")

    while True: #get input for quadrant rotation for black
        quad = input("Black, pick a quadrant to rotate (1,2,3,4): ")
        direction = input("Right or Left? (r,l): ")
        if (direction == 'r' or direction == 'R') and quad in "1234":
            board.rotateQuadrantRight(int(quad))
            break
        if (direction == 'l' or direction == 'L') and quad in "1234":
            board.rotateQuadrantRight(int(quad))
            break
        print("Not a valid input, Try again")
    board.printBoard()

    if board.checkVictory()==BLACK:
        print("Black Wins!")
        break
    elif board.checkVictory()==WHITE:
        print("White Wins!")
        break

    while True: #get input for marble placement for black
        move = input("White, place your marble (integer): ")
        if int(move) in range(36) and board.placeMarble(int(move),WHITE):
            break
        print("Not a valid position. Try again")
        
    while True: #get input for quadrant rotation for black
        quad = input("White, pick a quadrant to rotate (1,2,3,4): ")
        direction = input("Right or Left? (r,l): ")
        if (direction == 'r' or direction == 'R') and quad in "1234":
            board.rotateQuadrantRight(int(quad))
            break
        if (direction == 'l' or direction == 'L') and quad in "1234":
            board.rotateQuadrantRight(int(quad))
            break
        print("Not a valid input, Try again")
    board.printBoard()

    if board.checkVictory()==BLACK:
        print("Black Wins!")
        break
    elif board.checkVictory()==WHITE:
        print("White Wins!")
        break

